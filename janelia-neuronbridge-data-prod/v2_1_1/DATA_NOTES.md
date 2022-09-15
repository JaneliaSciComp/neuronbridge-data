### Release Version: 2.1.1

### Release Date: 2020-11-03

### Notes

* Fixed the merge process. There was a bug which favored matches with higher pixel score 
while merging results from EM-vs-MCFO with the results from EM-vs-SGal4 instead of the matches with a higher normalized gradient score.
 This led to a wrong ranking of the final results.

### Release Version: 2.1.0

### Release Date: 2020-09-15

#### EM data;
* Hemibrain 1.1
    * 32,777 EM bodies

#### LM data;
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

