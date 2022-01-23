# Soft computing

<h2>Goal</h2>
Goal of this project is to count how many times does ball bounce off the left or right wall in Brick Breaker game.

<h2>Dataset</h2>
Videos of Brick Breaker game and correct results are downloaded from <a href = https://drive.google.com/drive/folders/1plDgdCvoW-DngKjFDHNPl_XUaq8PzOqi>here</a>.

<h2>Steps</h2>
<ol>
  <li>
    <h4>Extrating edges</h4>
    <p>
      To get positions for left and right edge, I used CannyEdge method from openCV.
      Then to select lines from detected edges, I used HoughLinesP.
      To select left edge, I found the line with min value of x (since I'm looking only for vertical lines x1 and x2 are equal), and for the right edge with max value of x.
    </p>
  </li>
  <li>
    <h4>Extrating balls</h4>
    <p>
      To extract all balls from one frame, I used binary threshold and findContours method. Then I found contour which minimal enclosing circle radius matches ball radius.
    </p>
  </li>
  <li>
    <h4>Checking for contact</h4>
    <p>
      To detect whether ball made contact with one of the edges, I compared x value of ball center with x value of edge.
      In order to avoid counting same hit twice, I only consider hit if it happens in two unconsecutive frames.
    </p>
  </li>
</ol>

<h2>Results</h2>
With explained steps I managed to get MAE of 0.3

<h2>Requirements</h2>
<ol>
  <li>Python version == 3.7.0</li>
  <li>pip version == 21.3.1</li>
  <li>numpy version == 1.21.5</li>
  <li>opencv-python version == 4.5.5.62</li>
  <li>matplotlib version == 3.5.1</li>
  <li>IPython version == 7.31.1</li>
  <li>ipykernel version == 6.7.0</li>
  <li>jupyter_client version == 7.1.1</li>
  <li>jupyter_core version == 4.9.1</li>
  <li>jupyter_core version == 4.9.1</li>
  <li>nbclient version == 0.5.10</li>
  <li>notebook version == 6.4.7</li>
  <li>sklearn</li>
</ol>
These are version that I used, probably will work on higher versions.

<h2>How to run</h2>
<ul>
  <li>
    <h5>SOFT3.py<h5>
    <ol>
      <li>Install python and required packages</li>
      <li>Download zip and extract or git clone repository</li>
      <li>Open terminal or powershell window</li>
      <li>Type 'python SOFT3.py' in terminal window and hit ENTER</li>
    </ol>
  </li>
      
  <li>
    <h5>soft3jupt.ipynb<h5>
    <ol>
      <li>Install python and required packages</li>
      <li>Download zip and extract or git clone repository</li>
      <li>Open terminal or powershell window</li>
      <li>Type 'jupyter notebook' in terminal window and hit ENTER</li>
      <li>Find soft3jupt.ipynb and click on it</li>
      <li>Cell > Run All</li>
    </ol>
  </li>
</ul>
