# Step 19 - Comparator Descriptor Evidence Hardening

Verdict: `STEP19_REPOSITION_AS_ROTATABLE_MOBILITY_DESCRIPTOR_NOT_NEW_PRINCIPLE`

## pMSBP

- raw rho: -0.5315390888078491
- within-class residual rho: -0.269476413921309

## Top descriptor associations

- negative_rotatable_per_mw: residual rho=0.7028360779360622, n=7367
- rotatable_per_mw: residual rho=-0.7028360779360622, n=7367
- num_rings: residual rho=0.5549478352172701, n=7367
- num_aromatic_rings: residual rho=0.5326125359573793, n=7367
- num_rotatable_bonds: residual rho=-0.3238752161736721, n=7367
- heteroatom_density: residual rho=-0.27021483563839627, n=7367
- pmsbp_density: residual rho=-0.269476413921309, n=7367
- molecular_weight: residual rho=0.254823384474859, n=7367

## Incremental model audit

- pmsbp_only_within_class_residual_linear: R2=0.019470649786646477, delta=, n=7367
- base_comparators_within_class_residual_linear: R2=0.5782201581302235, delta=, n=7367
- base_plus_pmsbp_within_class_residual_linear: R2=0.5806365233200746, delta=0.0024163651898511107, n=7367

## Redundancy audit

- pMSBP vs molecular_weight: rho=-0.9801054611264118, n=7367
- pMSBP vs num_rings: rho=-0.8648894603509004, n=7367
- pMSBP vs num_aromatic_rings: rho=-0.8494666759736564, n=7367
- pMSBP vs num_hbond_acceptors: rho=-0.7507488730391669, n=7367
- pMSBP vs topological_surface_area: rho=-0.7323774549941539, n=7367
- pMSBP vs num_rotatable_bonds: rho=-0.5750368964113979, n=7367
- pMSBP vs heteroatom_density: rho=0.40580790489707047, n=7367
- pMSBP vs negative_rotatable_per_mw: rho=-0.3379226708705914, n=7367

## Interpretation

This audit decides whether the manuscript should be framed as an incremental descriptor result, a limited open-data observation, or a repositioned rotatable-mobility study.
