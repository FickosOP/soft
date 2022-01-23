# Soft computing

<h2>Goal</h2>
Goal of this project is to count how many times does ball bounce off the left or right wall in Brick Breaker game.

<h2>Dataset</h2>
Videos of Brick Breaker game and correct results are downloaded from <a href = https://drive.google.com/drive/folders/1plDgdCvoW-DngKjFDHNPl_XUaq8PzOqi>here</a>

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
  <li>sklearn</li>
</ol>
There are version that I used, probably will work on higher versions.

