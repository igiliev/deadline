import re

from grader import *


@test_cases([
    '1, 2, 3, 4, 5',
    '10, 10, 10, 10, 10, 10, 10, 10, 10',
    '5, 5, 5, 1, 2, 3, 4, 1, 4, 3',
    '0',
    '4310941, 2131, 132194, 149314, 141, 131, -1, -1, -1',
    '970.68, 7218.75, 6.41, 8.89, 0.64, 558.58, 780.67, 25135.15, 3915.16, 989.03, 86.11, 34.05, 566.91, 4.69, 24870.79, 830.33, 74.36, 810.62, 0.9, 23929.54, 35.63, 6429.82, 118.28, 99.21, 35.49, 2.71, 9460.22, 7102.5, 44.22, 64.26, 4.75, 84.58, 24.96, 88.85, 922.52, 69053.65, 4.94, 57.98, 7293.86, 8509.82, 4953.31, 7.54, 4.17, 1.56, 647.99, 45764.45, 2827.13, 180.72, 9003.35, 5773.21, 30446.41, 384.62, 419.53, 120.96, 58652.36, 786.55, 91531.71, 61583.6, 66315.63, 88.99, 343.16, 0.97, 9.18, 980.5, 9.45, 24.35, 1.17, 4.08, 9900.34, 5.43, 9.36, 19948.23, 650.14, 7.44, 966.11, 2756.34, 6.26, 9.15, 7.05, 5409.1, 6.44, 752.11, 18817.72, 95.63, 8356.04, 83818.68, 8.1, 80.1, 9.48, 7.32, 5.33, 121.2, 9600.57, 45.51, 64775.28, 118.53, 3482.16, 9048.42, 8219.94, 95.09, 91798.33, 249.15, 8535.9, 9030.59, 805.53, 7.32, 9.69, 119.19, 8.35, 17.17, 1.68, 21.92, 4.77, 998.21, 104.96, 8914.47, 63942.45, 6.54, 326.74, 90.08, 22.88, 6.02, 52.22, 183.26, 943.72, 89262.47, 4524.77, 4344.04, 214.74, 969.91, 27229.91, 7.23, 21.31, 46565.83, 9291.41, 4893.9, 811.84, 15069.59, 4.14, 1.77, 32624.4, 575.17, 38737.05, 8171.83, 5071.01, 69440.97, 7194.31, 361.69, 5062.98, 339.07, 2.31, 5.1, 7391.56, 94913.8, 757.94, 71.19, 47.88, 95.76, 4897.41, 1788.73, 6.86, 46584.31, 7056.48, 43.27, 8417.34, 60.84, 1050.02, 4.52, 436.57, 4849.85, 95345.98, 19801.72, 90684.56, 2.1, 702.8, 27.76, 989.8, 26.65, 388.82, 61648.91, 37.05, 22839.89, 50042.28, 7177.67, 8087.86, 82.29, 3574.38, 71.5, 1.29, 80159.09, 51360.77, 6674.11, 62784.16, 6919.69, 5831.2, 760.2, 6.54, 55.46, 72.41, 69.43, 15799.87, 891.51, 304.5, 344.51, 6.17, 30636.22, 416.51, 18732.27, 6006.7, 69290.55, 5.69, 4577.13, 97758.59, 5.49, 5627.16, 5728.12, 617.44, 9476.47, 0.31, 244.46, 6936.85, 84.8, 9671.69, 3.28, 76.77, 21537.56, 237.28, 330.21, 228.69, 53333.78, 77419.3, 872.03, 482.13, 7.07, 0.78, 0.07, 41.83, 20636.77, 78768.47, 75437.02, 4284.9, 12790.23, 96195.89, 53.56, 90988.28, 6398.43, 218.59, 30.8, 4289.33, 877.75, 2.42, 69.29, 32.19, 93.22, 32922.32, 6.88, 49.48, 3.91, 70132.04, 50528.02, 8.1, 25609.59, 418.41, 99489.31, 39.38, 0.31, 8877.69, 718.06, 152.09, 3824.09, 44723.47, 72222.49, 8845.9, 7999.57, 820.39, 21.59, 907.12, 9.26, 16736.07, 715.58, 5262.47, 6.97, 52331.37, 34.97, 77712.22, 228.31, 11509.5, 65243.18, 18.09, 726.4, 8851.07, 57.3, 9866.8, 94.4, 68.06, 31059.29, 86563.75, 789.17, 5.58, 26043.94, 2184.65, 6.07, 48875.37, 1.73, 3.58, 27744.14, 658.07, 43162.13, 976.09, 10.49, 1.5, 6231.03, 4839.24, 4297.04, 5.02, 461.71, 14.45, 46386.42, 54176.89, 770.09, 58649.27, 1.4, 7143.66, 35.44, 4.0, 1.14, 44.02, 47683.94, 1222.48, 990.65, 48.26, 43.31, 5.47, 15.73, 60.07, 1996.04, 6799.18, 6334.66, 84.28, 7.22, 7056.02, 5.69, 85.28, 59.8, 628.14, 48.92, 413.14, 19954.37, 96.53, 8893.3, 1.55, 931.88, 53244.65, 9481.19, 91045.46, 81935.83, 8.36, 46.8, 8679.29, 97147.04, 576.54, 47.7, 63.85, 72.98, 8.92, 7.83, 0.5, 8669.13, 1.89, 623.4, 5923.01, 2.3, 69.55, 6.68, 97.74, 5575.25, 2494.07, 17832.81, 68.86, 90.18, 1.22, 1.53, 4484.81, 143.68, 89.49, 66936.62, 8710.3, 1.25, 41625.78, 1.42, 9699.43, 6.0, 7379.44, 6768.73, 561.04, 67.17, 3912.93, 4.5, 428.32, 76219.19, 11163.84, 6420.36, 79055.37, 9076.16, 665.45, 8.74, 9353.6, 1869.98, 706.17, 1440.29, 59398.36, 2081.79, 7.61, 2665.11, 45.05, 7.71, 91.19, 6.78, 447.07, 115.48, 5.96, 5.58, 1.14, 1.61, 67063.84, 9.82, 7394.48, 9461.38, 9406.21, 201.35, 444.71, 198.49, 717.78, 596.0, 2.23, 94080.05, 8.35, 1.8, 7.63, 33016.3, 2534.09, 9079.08, 288.18, 7731.6, 7941.0, 3735.19, 18211.22, 34.42, 301.29, 3.29, 91.88, 1398.95, 351.79, 382.53, 3.93, 4911.43, 337.21, 0.62, 4.97, 3161.47, 1.6, 510.89, 6.47, 3013.29, 81.84, 598.84, 487.28, 22.17, 0.61, 15.08, 22.49, 7.79, 5999.34, 325.26, 65.58, 3733.61, 4.29, 7.82, 74.37, 6792.12, 36.78, 80302.54, 5634.07, 74679.08, 535.14, 4.9, 0.64, 7.74, 33.52, 7079.77, 20.2, 36.64, 1.8, 771.01, 0.95, 8683.09, 6.27, 8.81, 4.7, 25780.53, 19004.08, 29.14, 6198.83, 38.52, 20329.35, 5023.13, 5.36, 77159.36, 3.16, 704.41, 2.63, 4.62, 4689.51, 85.49, 72.17, 226.89, 9884.52, 1332.34, 39785.85, 40.91, 1.18, 10.26, 598.43, 8.81, 11.39, 948.36, 52.98, 1090.8, 66.35, 6735.65, 9672.25, 54.76, 1.73, 3516.42, 54750.67, 2774.89, 737.27, 9.68, 0.21, 6.25, 483.3, 8487.9, 9205.61, 34.03, 57.74, 576.31, 0.16, 9.63, 71.42, 734.91, 2425.82, 786.42, 5515.49, 81.54, 19.01, 58004.12, 9007.24, 101.45, 20.76, 2.73, 982.95, 3736.06, 3875.26, 737.91, 7.71, 105.23, 84.82, 64.41, 16.26, 9805.31, 9.51, 8.37, 545.27, 31091.87, 30.22, 2.71, 44214.61, 78525.06, 9534.85, 8.16, 43.0, 533.18, 7.1, 5.18, 75.98, 3.76, 6682.96, 400.64, 47479.56, 70.48, 3870.66, 2.01, 9.23, 139.61, 29.22, 4079.36, 71.55, 523.89, 360.93, 2357.39, 38.69, 87774.35, 9300.36, 3595.69, 56.27, 0.51, 97525.67, 9.44, 82.66, 70731.72, 9423.13, 56.89, 69.02, 6706.95, 91.56, 57719.39, 5151.92, 4.34, 36.75, 96.56, 2766.48, 88.14, 56.07, 46207.74, 25201.99, 64.75, 86654.14, 5950.44, 49.55, 56546.15, 2.55, 58.45, 42262.38, 66.27, 7.59, 80.32, 9.95, 94.39, 34539.77, 626.22, 471.8, 96.5, 7654.99, 3188.21, 2388.78, 5439.11, 79867.5, 234.55, 14.62, 45239.29, 85481.12, 9367.29, 452.23, 1.71, 98505.82, 82.38, 2.51, 480.38, 31029.01, 5.21, 9.67, 7.61, 9351.53, 21.42, 7252.8, 7213.01, 62.23, 251.39, 15053.89, 51268.5, 28.22, 26.82, 9.13, 534.07, 59404.32, 43244.87, 240.18, 9.53, 269.25, 21.86, 7234.61, 266.08, 51893.4, 334.93, 985.9, 3826.03, 88670.08, 523.98, 44.82, 0.36, 246.19, 32496.27, 19.09, 15333.43, 845.48, 572.64, 4061.36, 1.84, 591.6, 8766.59, 88.18, 634.65, 7103.96, 6022.19, 9.88, 746.41, 7903.99, 7.66, 49.83, 14.95, 11.11, 4504.45, 6567.67, 1038.94, 9676.13, 95299.91, 5089.06, 576.76, 43536.83, 49.6, 1.76, 8542.87, 9.95, 72171.41, 8.88, 7.29, 9.86, 450.88, 9.66, 7.95, 92.81, 583.5, 6004.08, 9.05, 8447.13, 730.28, 58079.24, 42.86, 91.26, 2.98, 843.78, 86.87, 773.63, 61461.32, 4.16, 496.63, 262.79, 907.65, 4.32, 763.16, 1424.69, 680.07, 9.5, 99358.56, 9602.93, 1.39, 38170.36, 6483.68, 2142.61, 9.37, 4.27, 88.97, 432.61, 88.59, 9.92, 3110.84, 46102.42, 3.37, 4.65, 5.08, 7095.77, 2850.58, 5.18, 30141.54, 3920.54, 17.28, 579.32, 391.38, 6076.16, 8.03, 9.36, 113.36, 171.14, 180.47, 17545.85, 103.55, 3.33, 4655.31, 25.4, 0.51, 40.0, 630.34, 47.1, 8662.33, 741.51, 55.3, 52848.9, 558.64, 989.28, 80.75, 67713.47, 35056.35, 926.81, 545.08, 50781.42, 2463.25, 2760.73, 78109.49, 33.1, 9.91, 283.59, 48.08, 5846.34, 72183.19, 42277.52, 3506.77, 548.18, 296.02, 178.72, 20.49, 10.42, 168.07, 25.1, 9033.62, 9.99, 852.61, 117.95, 102.36, 755.38, 2712.62, 1049.33, 175.08, 327.96, 61745.02, 91262.75, 1626.22, 4435.21, 8909.66, 76377.15, 14847.06, 5765.91, 62476.17, 2073.0, 81127.97, 9.92, 6.86, 6730.5, 3209.75, 82.31, 8.74, 8.17, 1.8, 4614.97, 6.83, 34.52, 9.82, 7098.53, 289.62, 7.61, 7839.26, 4.0, 879.57, 1.7, 19.78, 2045.92, 76.87, 3034.84, 7407.99, 3904.5, 60729.43, 5.27, 0.15, 231.07, 56.14, 8.08, 4.22, 77064.55, 9.04, 657.94, 1.6, 62822.89, 90.71, 3.36, 60.5, 56675.76, 14.68, 73.68, 316.99, 31.8, 4.11, 52.36, 44.6, 45.08, 55.09, 10.99, 58157.26, 12581.12, 99.63, 731.91, 7.79, 51.48, 5.28, 828.95, 3.4, 1300.03, 6460.21, 47374.29, 5094.78, 858.57, 0.73, 2400.54, 37.53, 4920.75, 1358.82, 46.99, 528.98, 77623.21, 40.22, 17.43, 2377.26, 2625.93, 84.33, 34.06, 9829.59, 901.89, 98559.34, 51.61, 206.18, 40291.5, 6634.62, 918.95, 4.96, 96029.14, 8.52, 140.68, 74.28, 392.71, 39.06, 4.95, 3370.23, 4737.12, 0.97, 85292.36, 9938.7, 993.29, 8.93, 52.36, 38.59, 194.37, 5.34, 407.34, 146.75, 443.69, 54803.58, 4339.38, 5244.52, 887.85, 4731.03, 165.01, 3813.0, 16.55, 1691.81, 63896.1, 55.7, 25.0, 5121.7, 94.07, 6095.99, 1940.64, 6987.57, 6.99, 154.45, 5965.58, 158.26, 461.9, 599.09, 9325.06, 3673.91, 6195.36, 12081.52, 9065.25, 31454.62, 72.27, 96.61, 66.6, 822.49, 4.4, 730.94, 61.14, 776.69, 75397.58, 4033.62, 6.54, 97020.87, 247.82, 2.12, 99.38, 975.14, 80086.86, 9.67',
    '1.2, -1.2'], description='Testing with numbers {}')
def search(m, given_str):
    m.stdin.put(given_str)
    given_output = re.sub(r'\s+', '', m.stdout.new())  # remove whitespaces
    expected_output = sum([float(p) for p in given_str.split(', ')])

    assert str(expected_output) == given_output, "{} is not equal to {}".format(expected_output, given_output)