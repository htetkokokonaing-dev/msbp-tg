# MSBP-Tg theory note 

## Core statement

Within comparable polymer chemistry-size fibers, normalized suppression of local rotatable mobility is associated with upward displacement of the glass-transition temperature (Tg) boundary.

## Descriptor transparency

MSBP density is exactly:

```text
rot_density = NumRotatableBonds / heavy_atoms
MSBP_density = -rot_density
```

The claim is not descriptor invention. The contribution is the use of this suppression-oriented coordinate as a boundary-level test inside comparable chemistry-size fibers.

## Physical mechanism

Tg marks the onset temperature for cooperative segmental chain motion. Repeat units with fewer rotatable bonds per heavy atom have lower local conformational freedom, so local rearrangements require higher thermal energy. MSBP density therefore approximates normalized resistance to local conformational motion.

## Why within-fiber testing is needed

Different polymer families carry different baseline Tg levels due to cohesion, polarity, packing, and backbone chemistry. Residualizing within comparable fibers removes those baselines and asks whether normalized local mobility suppression explains the remaining within-family Tg displacement.

## Why density is used

Raw rotatable-bond count is size-confounded. Larger repeat units can contain more rotatable bonds simply because they contain more atoms. Dividing by heavy-atom count converts raw count into a local rotational-freedom concentration.
