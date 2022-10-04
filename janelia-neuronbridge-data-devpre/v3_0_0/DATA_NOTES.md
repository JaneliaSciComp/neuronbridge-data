Model Version 3.0.0
* Switched to new data model
* No new data was added (no new images, no new matches)
* Merged Brain and VNC data from 2.4.0 and 2.3.0-pre
* All paths are absolute, optionally using prefix variables from config.json
* Eliminated all unnecessary attributes: maskImageURL, maskSampleRef, maskRelatedImageRefId, coverageScore, aggregateCoverage, matchingRatio, gradientAreaGap, highExpressionArea, normalizedGapScore

#### PatchPerPix (PPP) searches
Added PPPM results for VNC:0.5 dataset against GEN1 MCFO VNC samples.

#### Color Depth Searches

Added color depth searches for VNC:0.6 dataset against Split GAL4 and GEN1 MCFO samples.

**LM data**
* Added 3925 Split GAL4 and 32022 GEN1 MCFO VNC samples

**EM data**
* Added bodies for 2 EM VNC data sets
** 23128 VNC:0.6 bodies created on 2021-09-02
** 23358 VNC:0.5 bodies created on 2021-08-25

### Release Version: 2.4.0

### Release Date: 2022-02-25

#### Notes
* 3D files are available for download for both Color Depth Searches and PatchPerPix (PPP) searches
* LM data: aligned image stacks can be downloaded in the h5j format
* EM data: skeletons can be downloaded in the swc format

#### Color Depth Searches

**LM data**
* Added 27,600 additional samples from the Annotator Gen1 MCFO data set, including 579 new lines. These samples were imaged with 20x and 63x objectives instead of 40x. See the FlyLight Gen1 MCFO website (https://gen1mcfo.janelia.org/cgi-bin/gen1mcfo.cgi) for all available images and citation guidance.

The rest is as in [2.2.0](###Release-Version:-2.2.0)

### Release Version: 2.3.0

### Release Date: 2021-10-26

#### Color Depth Searches

**LM data**
* Added MCFO phase 2 lines

The rest is as in [2.2.0](###Release-Version:-2.2.0)

### Release Version: 2.2.1

### Release Date: 2021-10-18

#### Color Depth Searches

See [2.2.0](###Release-Version:-2.2.0)

#### PatchPerPix (PPP) searches
**EM data**
* Hemibrain 1.2.1

**LM data**
* MCFO Phase 2

**Notes**
* See https://github.com/Kainmueller-Lab/PatchPerPix for information on the algorithm

### Release Version: 2.2.0

### Release Date: 2021-09-30

#### Color Depth Searches

**EM data**
* Hemibrain 1.2.1

**LM data**
* MCFO GAL4 lines
* Stable split GAL4 lines

* Parameters for pre-computed color-depth matches between LM and EM data 
    * maskThreshold: 20
    * targetThreshold: 20
    * xyShift : 2
    * mirrorMask: enabled
    * pixColorFluctuation: 1.0
    * pctPositivePixels: 1.0

**Notes** 
* Added `neuronType` and `neuronInstance` attributes to EM results JSON
* Added `searchablePNG` attribute to results JSON

#### PatchPerPix (PPP) searches
**EM data**
* Hemibrain 1.2.0

**LM data**
* MCFO GAL4 lines

**Notes**
* See https://github.com/Kainmueller-Lab/PatchPerPix for information on the algorithm


### Release Version: 2.1.1

### Release Date: 2020-11-03

### Notes

* Fixed the merge process. There was a bug which favored matches with higher pixel score
while merging results from EM-vs-MCFO with the results from EM-vs-SGal4 instead of the matches 
with a higher normalized gradient score. This led to a wrong ranking of the final results.
 
### Release Version: 2.1.0

### Release Date: 2020-09-15

#### EM data
* Hemibrain 1.1
    * 32,777 EM bodies

#### LM data
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

* Parameters for pre-computed matches between LM and EM data 
    * maskThreshold: 20
    * targetThreshold: 20
    * xyShift : 2
    * mirrorMask: enabled
    * pixColorFluctuation: 1.0
    * pctPositivePixels: 1.0


### Notes
* Data format change - removed the attributes map


### Release Version: 1.1.0

### Release Date: 2020-04-15

### Notes
* Precomputed matches between Flylight Split GAL4 and MCFO vs Hemibrain 1.0.1
* Created the segmentation for Flylight Split GAL4 and MCFO libraries and
the color depth search between hemibrain neurons and flylight was actually run
using the segmented MIPs
* For Hemibrain neurons which cross the middle section also
generated the flipped neuron by mirroring it and adding the original
and also compared this against all flylight MIPs.
* For calculating the negative scores - gradient area gap 
and the area of regions with high expression - we selected the MIPs for the top 300 lines
and we used precomnputed RGB masks generated with a radius of 20px
