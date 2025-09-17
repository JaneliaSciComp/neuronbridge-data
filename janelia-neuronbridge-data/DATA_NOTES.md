## Data Version 3.7.2 (released TBD)

**New LM Split-GAL4 data sets**

In this data release we have added the first half of a large collection of split-GAL4 driver lines, including both additional Stable Split (SS) and a new set of temporary Initial Split (IS) lines, from the recent [FlyLight Split-GAL4 Omnibus Broad release](https://doi.org/10.1101/2024.01.09.574419). We also added images from recently published [split-GAL4 papers](https://splitgal4.janelia.org/cgi-bin/splitgal4.cgi). Counts are given as "# searchable CDMs (# source images)".

* [Split-GAL4 Omnibus Broad](https://doi.org/10.1101/2024.01.09.574419)
  * Brain (Batch1) 61051 (33612)
  * Brain (Batch3) 25091 (14622)
  * Brain (Batch4) 28695 (17623)
  * VNC: 290285 (88430)
* [Gorko et al 2024](https://doi.org/10.1038/s41586-024-07222-5)
  * Brain: 37 (28)
  * VNC: 74 (36)
* [Nern et al 2024](https://doi.org/10.1101/2024.04.16.589741)
  * Brain: 23865 (10324)
  * VNC: 1511 (819)
* [Schretter et al 2024](https://doi.org/10.1038/s41586-024-08255-6)
  * Brain: 26 (21)
  * VNC: 6 (4)
* [Descending Neurons 2025](https://doi.org/10.1101/2025.02.22.639679)
  * Brain: 779 (502)
  * VNC: 782 (505)
* [Split-GAL4 Omnibus Rescreen](https://doi.org/10.1101/2024.01.09.574419)
  * Brain: 14 (2)
  * VNC: 7 (7)
* [Wolff et al 2024](https://doi.org/10.1101/2024.10.21.619448)
  * Brain: 3119 (2430)
  * VNC: 659 (401)

**Additional MANC data**

* Added 24350 VNC neuron bodies from the newest (MANC 1.2.1) [FlyEM MANC release](https://www.janelia.org/project-team/flyem/manc-connectome)

* CNS
  * Brain 128780 (109409)
  * VNC 5411 (3849)

## Data Version 3.4.0 (released on 2024-10-30)

### Color Depth Searches

**New LM Split-GAL4 data sets**

In this data release we have added a collection of cell-type-specific split-GAL4 driver lines (the initial splits or "IS" lines) from the recent [FlyLight Split-GAL4 Omnibus Broad release](https://doi.org/10.1101/2024.01.09.574419).
* [Split-GAL4 Omnibus Broad](https://doi.org/10.1101/2024.01.09.574419)
  * Brain: 101486 (34012)
  * VNC: 61854 (28424)


## Data Version 3.3.2 (released on 2024-10-16)

### Color Depth Searches

**Flywire v783 data set**

We imported SWC files and selected annotation metadata for the [FlyWire Brain v783 data set](http://dx.doi.org/10.1038/s41586-024-07558-y) (excluding any neurons with an "optic" annotation e.g. super class, since NeuronBridge does not yet support matching in the optic lobes). These 61,750 neurons were subsequently transformed to the common alignment space and exported as Color Depth MIPs. We then precomputed matches between the FlyWire Brain data set and all the current FlyLight image collections (Split GAL4, Gen1 MCFO, Gen1 Annotator MCFO). We eliminated matches with a pixel score less than 3.5%. As with the FlyEM Hemibrain, we then selected the top 300 lines for gradient scoring, but to improve performance we also restricted the number of samples to the top 3 samples per line. 

## Data Version 3.2.1 (released on 2024-03-22)

### Color Depth Searches

**LM Split-GAL4 data sets**

We added 235 brain images (derived from 94 source images) that we missed from [Split-GAL4 Omnibus Rescreen](https://doi.org/10.1101/2024.01.09.574419) in 3.2.0. These images are part of 48 lines that were updated, 3 of which are completely new.

## Data Version 3.2.0 (released on 2024-03-11)

### Color Depth Searches

**New LM Split-GAL4 data sets**

In this data release we have added a collection of cell-type-specific split-GAL4 driver lines from the recent FlyLight preprint, as well as other recently published [split-GAL4 papers](https://splitgal4.janelia.org/cgi-bin/splitgal4.cgi). Counts are given as "# searchable CDMs (# source images)".

* [Split-GAL4 Omnibus Rescreen](https://doi.org/10.1101/2024.01.09.574419)
  * Brain: 11562 (5173)
  * VNC: 7595 (4135)

* [Ascending Neurons 2023](https://doi.org/10.25378/janelia.23726103)
  * Brain: 201 (88)
  * VNC: 114 (86)

* [Cheong, Boone, Bennett 2023](https://doi.org/10.1016/j.cub.2024.01.071)
  * Brain: 3 (3)
  * VNC: 6 (3)

* [Cheong, Eichler, Stuerner 2023](https://doi.org/10.1101/2023.06.07.543976)
  * Brain: 6 (4)
  * VNC: 103 (62)

* [Dorsal VNC 2023](https://doi.org/10.1101/2023.05.31.542897)
  * Brain: 4491 (2509)
  * VNC: 7925 (5659)

* [Isaacson et al 2023](https://doi.org/10.1101/2023.06.21.546024)
  * Brain: 524 (201)
  * VNC: 59 (16)

* [Lillvis 2022](https://doi.org/10.7554/eLife.81248)
  * Brain: 11 (2)
  * VNC: 9 (2)

* [Lillvis 2023](https://doi.org/10.1016/j.cub.2024.01.015)
  * Brain: 954 (219)
  * VNC: 496 (261)

* [oviDN 2023](https://doi.org/10.1038/s41586-023-06271-6)
  * Brain: Brain: 203 (132)
  * VNC: 83 (50)

* [Rubin & Aso 2023](https://doi.org/10.7554/eLife.90523)
  * Brain: 278 (159)
  * VNC: 28 (20)

* [Yoo et al 2023](https://doi.org/10.1016/j.cub.2023.08.020)
  * Brain: 378 (109)
  * VNC: 30 (10)


**Updated LM Split-GAL4 data sets**

We also updated releases where some images were previously missing from NeuronBridge:

* Aso 2021
  * Brain: 30563 (13974)
  * VNC: 6779 (2440)

* DNp13 2020
  * Brain: 49 (15)
  * VNC: 25 (13)

* Longden_et_al_2021
  * Brain: 44 (12)
  * VNC: 0

* MB Paper 2014
  * Brain: 1515 (641)
  * VNC: 486 (236)

* Optic lobe TAPIN-Seq 2020
  * Brain: 349 (112)
  * VNC: 162 (51)

* SEZ 2021
  * Brain: 4176 (2060)
  * VNC: 1648 (506)

* T4_inputs_paper
  * Brain: 67 (18)
  * VNC: 17 (6)


## Data Version 3.1.1 (released on 2023-07-08)

### Color Depth Searches

**LM data**
* Added 43,393 additional Split GAL4 brain color depth MIPs

**EM data**
* Added 23,271 Male VNC neuron bodies from the [FlyEM MANC release](https://www.janelia.org/project-team/flyem/manc-connectome)
 and computed precomputed matches against all LM VNC images.

### PatchPerPix (PPP) searches
Added PPPM results for VNC:0.5 data set against Gen1 MCFO VNC samples.


## Data Version 3.0.0 (released on 2023-02-01)

### Data Model
* Switched to new data model
* No new data was added (no new images, no new matches)
* Merged Brain and VNC data from 2.4.0 and 2.3.0-pre
* All paths are absolute, optionally using prefix variables from config.json
* Removed unused attributes: `maskImageURL`, `maskSampleRef`, `maskRelatedImageRefId`, `coverageScore`, 
  `aggregateCoverage`, `matchingRatio`, `gradientAreaGap`, `highExpressionArea`, `normalizedGapScore`.
* The data migration from 3.0.0 eliminated all LM to EM matches that actually did not have a gradient score. 
  Those matches were originally exported due to a bug in v2.x which inadvertently exported LM to EM match that did not have 
  a gradient score when the EM to LM gradient scores were updated for the corresponding LM to EM matches.


## Data Version 2.4.0 (released on 2022-02-25)

### Data Model
* 3D files are available for download for both Color Depth Searches and PatchPerPix (PPP) searches
* LM data: added aligned image stacks in the H5J format
* EM data: added skeletons in the SWC format

### Color Depth Searches

**LM data**
* Added 27,600 additional samples from the Annotator Gen1 MCFO data set, including 579 new lines. These samples were imaged with 20x and 63x objectives instead of 40x. 
* See the [FlyLight Gen1 MCFO website](https://gen1mcfo.janelia.org/cgi-bin/gen1mcfo.cgi) for all available images and citation guidance.


## Data Version 2.3.0 (released on 2021-10-26)

### Color Depth Searches

**LM data**
* Added MCFO phase 2 lines


## Data Version 2.2.1 (released on 2021-10-18)

### PatchPerPix (PPP) searches

**EM data**
* Hemibrain 1.2.1

**LM data**
* MCFO Phase 2

### Notes
* See [PatchPerPix website](https://github.com/Kainmueller-Lab/PatchPerPix) for information on the PPPM algorithm


## Data Version 2.2.0 (released on 2021-09-30)

### Data Model
* Added `neuronType` and `neuronInstance` attributes to EM results JSON
* Added `searchablePNG` attribute to results JSON

### Color Depth Searches

**EM data**
* Hemibrain 1.2.1

**LM data**
* MCFO GAL4 lines
* Stable split GAL4 lines

Parameters for pre-computed color-depth matches between LM and EM data:
* maskThreshold: 20
* targetThreshold: 20
* xyShift : 2
* mirrorMask: enabled
* pixColorFluctuation: 1.0
* pctPositivePixels: 1.0


### PatchPerPix (PPP) searches
**EM data**
* Hemibrain 1.2.0

**LM data**
* MCFO GAL4 lines


## Data Version 2.1.1 (released on 2020-11-03)

* Fixed the merge process. There was a bug which favored matches with higher pixel score while merging results from 
  EM-vs-MCFO with the results from EM-vs-SplitGal4 instead of the matches with a higher normalized gradient score. This 
  led to a wrong ranking of the final results.
 

## Data Version 2.1.0 (released on 2020-09-15)

### Data Model
* Data format change - removed the attributes map

### Color Depth Searches

**EM data**
* Hemibrain 1.1
    * 32,777 EM bodies

**LM data**
* MCFO GAL4 lines
   * 175,533 segmented MCFO CDM
   * 80,812 MCFO channels
   * 27,144 MCFO samples
   * 4,540 MCFO GAL4 lines

* Stable split GAL4 lines
   * 8,727 segmented SS CDM
   * 3,045 SS channels
   * 1,379 SS samples
   * 653 SS lines

### Notes
Parameters for pre-computed matches between LM and EM data:
* maskThreshold: 20
* targetThreshold: 20
* xyShift : 2
* mirrorMask: enabled
* pixColorFluctuation: 1.0
* pctPositivePixels: 1.0


## Data Version 1.1.0 (released on 2020-04-15)

* Precomputed matches between Flylight Split GAL4 and MCFO vs Hemibrain 1.0.1.
* Created the segmentation for Flylight Split GAL4 and MCFO libraries and the color depth search between Hemibrain 
  neurons and FlyLight images was actually run using the segmented MIPs.
* For Hemibrain neurons which cross the middle section also generated the flipped neuron by mirroring it and adding 
  the original and also compared this against all FlyLight MIPs.
* For calculating the negative scores - gradient area gap and the area of regions with high expression - we selected 
  the MIPs for the top 300 lines and we used precomnputed RGB masks generated with a radius of 20px.

