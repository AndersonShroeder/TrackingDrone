# TrackingDrone
<h2>Methodology</h2>
<p>The program is broken up into two main components. </p>
<p> 1. A FlightControl class which contains all relevant information and modifying functions involving 
the position, speed, direction and indicators for autonomous flight. </p>
<p> 2. A Mediacontrol class, which is responsible for the UI and detections. If there are any detections the vision object of Flightcontrol is modified by Mediacontrol.

<h2>Features</h2>
<h3>Manual Flight</h3>
<p>A fully functional manual flight mode which allows user control of the drone. This includes variations in speed and direction, the ability
to move up and down as well as the ability to take off and land on command.</p>
<p>These features require no additonal input to enable at runtime and the implementation for these features can be found under the FlightControl class located in the Main.py file. </p>
<h3>Autonomous Flight</h3>
<p> All features of the autonomous flight are initialized on initialization of FlightControl. Therefore, they must be enabled prior to running the program by adjusting the appropriate boolean values in the
call for the FlightControl class within the main function of Main.py.</p>
<h4>Hand Controls</h4>
<p>Utlizing pose estimation of the hands, the drone accepts a raised index finger to indicate a shift to autonomous flight and a raised index and middle finger
to shift into manual flight. This is done by changing the auto attribute of the Flight Control Class.
<h4>Face Tracking</h4>
<p>The drone supports face detection which is done by detecting a face and drawing a bounding box around the detected face. Additionally, while in autonomous flight,
the drone will begin a "follow" protocol and maintain a certain distance - which is established by pixel area of the bounding box since smaller area corresponds with 
a greater distance from the drone - as well as maintaining the center of the face in the center of the streamed video. The drone will automatically adjust speed
to match the speed of the detected face if it moves. </p>

<h2>How To Use </h2>
<p> Upon running the program while the drone is connected via wifi, pressing "t" will initialize flight and begin take off. At this point the drone
is in manual flight and can be: </p>
<p>1. Moved forward utilizing the "up" and "down" arrow keys.</p>
<p>2. Moved left and right utilizing the "left" and "right" arrow keys.</p>
<p>3. Moved up and down by uutilizing the "w" and "s" keys.</p>
<p>4. Rotated right and left by using the "q" and "e" keys.</p>
<p>5. Shifted to autonomous mode by pressing "a".</p>
<p>Once in autonomous mode the drone will begin searching for a face to track. Once it has found a face to track, it will begin maintaining the face in
the center of the frame as well as an appropriate following distance. At this point autonomous mode can be disabled by either: </p>
<p>1. Utilizing the hand pose tracker and raising the index/middle finger to shift to manual flight.</p>
<p>2. Pressing the "m" key. </p>
