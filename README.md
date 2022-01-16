## Video Seam Carving

In this project, we decided to implement seam carving for videos. We conducted a literature review and we decided to implement the approach mentioned in the paper *Discontinuous Seam-Carving for Video Retargeting* from Google and Georgia Tech. We choose this paper primarily because its approach is unique and interesting. Rather than using a 3D pixel matrix, the authors suggest using a temporal and spatial cost function to measure the pixels energy map. Then based on the forward energy map, we go back and reselect the seams based on its energy map and forward energy costs.

In our implementation, we used *SKImage* as a tool to help us preprocess each image frame for faster video seam carving.

#### Implement Temporal Coherence

Given successively computed seams $S^i$ in every $m\times n$ frame $F^i$ with $i \in {1,\dots , T}$ .  After removing a seam, the adjusted $(m-1)\times n$ frames $R^i$ should be similar to the nearest temporally coherent frame $R^c$.  By using $R^c$ as a factor to select $S^i$ in this pass forward methodology, for every pixel $(x, y)$, we can explicitly calculate the difference from $R^i$ to $R^c$.  The formula we use to measure temporal coherence, $T_c(x, y)$  is below:
$$
T_c = \sum_{k=0}^{x-1} \lVert F_{k,y}^i - R_{k,y}^c\rVert^2 + \sum_{k=x+1}^{m-1} \rVert F_{k,y}^i - R_{k-1, y}^c\lVert^2
$$

In our code, we have a special function to calculate the total temporal cost matrix by calling a seam-carving on the current frame using the current seam and then based on the output we produce a new matrix that is the difference between the current frame and the new processed frame. This matrix is used in the final calculation of the total costs.

#### Implement Spatial Coherence

Spatial cost matrix is the same as forward energy map. We use the previous frame seams and use the energy map to produce the next frame energy map after the seam-carving is done. Then the spatial difference is the forward energy map and the current energy map. It is also a component to the final cost matrix.

<img src="img\spatial.PNG" style="zoom:50%;" />

![S'_v(x_b, x_a, y) = \sum_{k=x_a}^{x_b-1} \lvert G_{k,y}^v-G_{k,y}^d\rvert + \sum_{k=x_a+1}^{x_b} \lvert G_{k,y}^v - G_{k-1,y}^d\rvert](https://latex.codecogs.com/svg.latex?\Large&space;S'_v(x_b, x_a, y) = \sum_{k=x_a}^{x_b-1} \lvert G_{k,y}^v-G_{k,y}^d\rvert + \sum_{k=x_a+1}^{x_b} \lvert G_{k,y}^v - G_{k-1,y}^d\rvert) 

#### Combining both temporal and spatial coherence

Finally we add up the temporal and spatial cost matrix and use it to come up with the new seam using traditional dynamic Programming. Then we cut the seams accordingly frame by frame.

---

#### Graphic UI

We use *tkinter* package for wrapping the codes into a user-friendly interface, screenshots as following:

The GUI passes variables to the backend video seam carving program and exhibits the result carved video after the process is done. The user need to choose the carving type in the first place (vertical/horizontal) and type in the number of seam lines that is going to be removed from the original video. Then the user clicks "Cut set" button and the backend will pop up a window that indicates the variables passed in. After this step, the user can click "Select File" button to choose an input video to be seam carved. After the input has been set, an information window about the basic parameters of the video such as *fps* and *number of frames* will appear on screen. The user can set the output file name by then. Our program supports *mp4* and *m4v* file format for output based on *mp4*, *m4v* and *avi* format. After the output file name has been set, the user can click run to proceed. 



<table><tr> <td> <img src="img\GUI2.PNG" alt="Drawing" style="width: 325px; height: 300px;"/> </td> <td> <img src="img\GUI4.PNG" alt="Drawing" style="width: 325px; height: 300px;"/> </td> </tr></table>



The program will display the carving result frame by frame in a pop up window. The window will disappear after the carving process is done. Output file will be saved at the designated directory. The user can click "Play" button to view the comparison between the input and the output. Two videos will play side by side to show the difference.

 







#### Example Result

<table><tr> <td> <img src="img\Original.PNG" alt="Drawing" style="width: 500px;"/> </td> <td> <img src="img\Carved.PNG" alt="Drawing" style="width: 300px;"/> </td> </tr></table>

---

#### References

1. Grundmann, Matthias, et al. "Discontinuous seam-carving for video retargeting." Georgia Institute of Technology, 2010.
2. Rubinstein, Michael, Ariel Shamir, and Shai Avidan. "Improved seam carving for video retargeting." *ACM transactions on graphics (TOG)*. Vol. 27. No. 3. ACM, 2008.
3. Yan, Bo, Kairan Sun, and Liu Liu. "Matching-area-based seam carving for video retargeting." *IEEE Transactions on circuits and systems for video technology* 23.2 (2012): 302-310.
4. Shamir, Ariel, and Shai Avidan. "Seam carving for media retargeting." *Communications of the ACM* 52.1 (2009): 77-85.
