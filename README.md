<h1>TrackingDrone</h1>

<h2>Introduction</h2>

<p>TrackingDrone is a drone application that allows users to control a drone either manually or autonomously. It provides the user with the ability to track and follow a target using face tracking and hand controls.</p>

<h2>System Requirements</h2>

<p>A drone that is compatible with the application
A computer with the following specifications:</p>
<ul>
<li>Operating system: Windows or macOS</li>
<li>RAM: 8GB or more</li>
<li>CPU: Intel i5 or equivalent</li>
<li>Graphics card: NVIDIA GTX 1050 or equivalent</li>
</ul>

<h2>Installation</h2>

<h3>To install TrackingDrone, follow these steps:</h3>

<ol>
<li>Install any necessary dependencies, such as the drone software and the OpenCV library.</li>
<li>Clone the TrackingDrone repository to your local machine.</li>
<li>Connect the drone to your computer via wifi.</li>
<li>Run the main.py file to start the application.</li>
</ol>

<h2>Features</h2>

<h3>TrackingDrone includes the following features:</h3>

<h4>Manual Flight</h4>
<p>TrackingDrone includes a fully functional manual flight mode, which allows the user to control the drone's position, speed, direction, and altitude. This feature is available as soon as the program is launched and requires no additional input to enable.</p>

<h4>Autonomous Flight</h4>
<p>The autonomous flight feature of TrackingDrone is initialized on startup of the application. The user can enable this feature by adjusting the appropriate boolean values in the FlightControl class located in the Main.py file.</p>

<h4>Hand Controls</h4>

<p>Utilizing pose estimation of the hands, the drone accepts a raised index finger to indicate a shift to autonomous flight and a raised index and middle finger to shift into manual flight. This is done by changing the auto attribute of the Flight Control Class.</p>

<h4>Face Tracking</h4>

<p>The drone supports face detection which is done by detecting a face and drawing a bounding box around the detected face. Additionally, while in autonomous flight, the drone will begin a "follow" protocol and maintain a certain distance, which is established by pixel area of the bounding box since smaller area corresponds with a greater distance from the drone, as well as maintaining the center of the face in the center of the streamed video. The drone will automatically adjust speed to match the speed of the detected face if it moves.</p>

<h2>Examples</h2>

<h3>TrackingDrone can be used in a variety of real-world scenarios, such as:</h3>

<ul>
<li>Tracking a person or object during a search and rescue mission</li>
<li>Filming an outdoor event or sports activity</li>
<li>Providing aerial surveillance in a security or military setting</li>
</ul>

<h2>Methodology</h2>

<h3>The program is broken up into two main components:</h3>

<p>A FlightControl class which contains all relevant information and modifying functions involving the position, speed, direction, and indicators for autonomous flight.</p>
<p>A Mediacontrol class, which is responsible for the UI and detections. If there are any detections, the vision object of Flightcontrol is modified by Mediacontrol.</p>

<h2>How To Use</h2>

<h3>To use TrackingDrone, follow these steps:</h3>
<ol>
<li>Connect the drone to your computer via wifi.</li>
<li>Run the main.py file to start the application.</li>
<li>Press "t" to initialize flight and begin takeoff.</li>
<li>In manual flight mode, use the arrow keys to move the drone and the "q" and "e" keys to rotate it.</li>
<li>To switch to autonomous flight, press "a".</li>
<li>Once in autonomous mode, the drone will begin searching for a face to track. Once it has found a face to track, it will begin maintaining the face in the center of the frame as well as an appropriate following distance.</li>
<li>To switch back to manual flight mode, either utilize the hand pose tracker and raise the index/middle finger or press the "m" key.</li>
</ol>
