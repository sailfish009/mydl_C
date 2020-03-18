mydl.modeling package
===========================

.. automodule:: mydl.modeling
    :members:
    :undoc-members:
    :show-inheritance:


mydl.modeling.poolers module
---------------------------------------

.. automodule:: mydl.modeling.poolers
    :members:
    :undoc-members:
    :show-inheritance:


mydl.modeling.sampling module
------------------------------------

.. automodule:: mydl.modeling.sampling
    :members:
    :undoc-members:
    :show-inheritance:


mydl.modeling.box_regression module
------------------------------------------

.. automodule:: mydl.modeling.box_regression
    :members:
    :undoc-members:
    :show-inheritance:


Model Registries
-----------------

These are different registries provided in modeling.
Each registry provide you the ability to replace it with your customized component,
without having to modify mydl's code.

Note that it is impossible to allow users to customize any line of code directly.
Even just to add one line at some place,
you'll likely need to find out the smallest registry which contains that line,
and register your component to that registry.


.. autodata:: mydl.modeling.META_ARCH_REGISTRY
.. autodata:: mydl.modeling.BACKBONE_REGISTRY
.. autodata:: mydl.modeling.PROPOSAL_GENERATOR_REGISTRY
.. autodata:: mydl.modeling.RPN_HEAD_REGISTRY
.. autodata:: mydl.modeling.ANCHOR_GENERATOR_REGISTRY
.. autodata:: mydl.modeling.ROI_HEADS_REGISTRY
.. autodata:: mydl.modeling.ROI_BOX_HEAD_REGISTRY
.. autodata:: mydl.modeling.ROI_MASK_HEAD_REGISTRY
.. autodata:: mydl.modeling.ROI_KEYPOINT_HEAD_REGISTRY
