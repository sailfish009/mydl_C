# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
"""
DensePose Training Script.

This script is similar to the training script in mydl/tools.

It is an example of how a user might use mydl for a new project.
"""

import os

import mydl.utils.comm as comm
from mydl.checkpoint import DetectionCheckpointer
from mydl.config import get_cfg
from mydl.data import build_detection_test_loader, build_detection_train_loader
from mydl.engine import DefaultTrainer, default_argument_parser, default_setup, launch
from mydl.evaluation import COCOEvaluator, DatasetEvaluators, verify_results
from mydl.utils.logger import setup_logger

from densepose import DatasetMapper, DensePoseCOCOEvaluator, add_densepose_config


class Trainer(DefaultTrainer):
    @classmethod
    def build_evaluator(cls, cfg, dataset_name):
        output_folder = os.path.join(cfg.OUTPUT_DIR, "inference")
        evaluators = [COCOEvaluator(dataset_name, cfg, True, output_folder)]
        if cfg.MODEL.DENSEPOSE_ON:
            evaluators.append(DensePoseCOCOEvaluator(dataset_name, True, output_folder))
        return DatasetEvaluators(evaluators)

    @classmethod
    def build_test_loader(cls, cfg, dataset_name):
        return build_detection_test_loader(cfg, dataset_name, mapper=DatasetMapper(cfg, False))

    @classmethod
    def build_train_loader(cls, cfg):
        return build_detection_train_loader(cfg, mapper=DatasetMapper(cfg, True))


def setup(args):
    cfg = get_cfg()
    add_densepose_config(cfg)
    cfg.merge_from_file(args.config_file)
    cfg.merge_from_list(args.opts)
    cfg.freeze()
    default_setup(cfg, args)
    # Setup logger for "densepose" module
    setup_logger(output=cfg.OUTPUT_DIR, distributed_rank=comm.get_rank(), name="densepose")
    return cfg


def main(args):
    cfg = setup(args)

    if args.eval_only:
        model = Trainer.build_model(cfg)
        DetectionCheckpointer(model, save_dir=cfg.OUTPUT_DIR).resume_or_load(
            cfg.MODEL.WEIGHTS, resume=args.resume
        )
        res = Trainer.test(cfg, model)
        if comm.is_main_process():
            verify_results(cfg, res)
        return res

    trainer = Trainer(cfg)
    trainer.resume_or_load(resume=args.resume)
    return trainer.train()


if __name__ == "__main__":
    args = default_argument_parser().parse_args()
    print("Command Line Args:", args)
    launch(
        main,
        args.num_gpus,
        num_machines=args.num_machines,
        machine_rank=args.machine_rank,
        dist_url=args.dist_url,
        args=(args,),
    )
