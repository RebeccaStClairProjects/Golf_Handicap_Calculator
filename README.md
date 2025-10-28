<h1 style="text-align:center; font-size:2.5em;">Golf Handicap Calculator (Full-Stack Web Platform)</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Language-Python-blue.svg" alt="Python Badge"/>
  <img src="https://img.shields.io/badge/Framework-Flask-green.svg" alt="Flask Badge"/>
  <img src="https://img.shields.io/badge/Database-MySQL-orange.svg" alt="MySQL Badge"/>
  <img src="https://img.shields.io/badge/Front--End-HTML%2FCSS%2FJS-yellow.svg" alt="Frontend Badge"/>
  <img src="https://img.shields.io/badge/License-MIT-lightgrey.svg" alt="License Badge"/>
</p>

<p style="font-size:1.1em;">An evolving full-stack web platform designed to simplify golf handicap tracking and promote transparency across competitive play. Built with <b>Python (Flask)</b>, <b>MySQL</b>, and a responsive front-end, this project bridges back-end logic and front-end design to create an intuitive, data-driven experience for club members.</p>

<blockquote><b>Who this is for:</b> Reviewers of my internship portfolio and peers interested in practical, self-directed full-stack development that connects code, data, and user experience.</blockquote>

<hr>

<h2>Table of Contents</h2>
<ul>
  <li><a href="#overview">Overview</a></li>
  <li><a href="#philosophy">Development Philosophy</a></li>
  <li><a href="#techstack">Tech Stack</a></li>
  <li><a href="#architecture">Architecture Overview</a></li>
  <li><a href="#collaboration">Client Collaboration</a></li>
  <li><a href="#features">Key Features</a></li>
  <li><a href="#roadmap">Future Development Roadmap</a></li>
  <li><a href="#about-developer">About the Developer</a></li>
  <li><a href="#license">License</a></li>
</ul>

<hr>

<h2 id="overview">Overview</h2>
<p>This project represents an ongoing, self-guided exploration of full-stack web development — connecting Python and MySQL through Flask to build a functional, reliable, and user-centered scoring system. The platform allows golfers to record scores, calculate handicaps, and understand how their performance evolves over time.</p>

<p>The backend database is hosted on <b>HelioHost</b>, enabling real-world testing with live data shared between developer and club members. Webpages are actively developed in Visual Studio and GitHub and will be deployed to HelioHost once core features are finalized.</p>

<hr>

<h2 id="philosophy">Development Philosophy</h2>
<p><i>“Bringing imagination and engineering together — one line of code at a time.”</i></p>
<p>Built from the belief that technology should clarify, not complicate. Every line of code aims to make complex golf calculations intuitive and understandable. Designed with empathy for non-technical users, the system focuses on transparency, data accuracy, and user trust — turning raw numbers into meaningful insight.</p>

<hr>

<h2 id="techstack">Tech Stack</h2>
<table>
  <tr><th>Layer</th><th>Technology</th><th>Purpose</th></tr>
  <tr><td>Front-End</td><td>HTML, CSS, JavaScript</td><td>Responsive forms and display templates</td></tr>
  <tr><td>Back-End</td><td>Python (Flask)</td><td>Routing, server logic, data validation</td></tr>
  <tr><td>Database</td><td>MySQL (HelioHost)</td><td>Player, score, and course data management</td></tr>
  <tr><td>Visualization</td><td>Chart.js (Planned)</td><td>Data-driven dashboards and insights</td></tr>
  <tr><td>Deployment</td><td>HelioHost / GitHub</td><td>Remote testing and collaborative development</td></tr>
  <tr><td>Version Control</td><td>Git / GitHub</td><td>Collaboration and history tracking</td></tr>
</table>

<hr>

<h2 id="architecture">Architecture Overview</h2>
<pre>
Golf_Handicap_Calculator/
  static/                 // CSS, JS, and images
  templates/              // HTML templates (Flask Jinja)
  app.py                  // Main Flask entry point
  routes/                 // Organized Flask routes (planned)
  db/                     // SQL scripts and schema definitions
  config.py               // Connection settings and environment variables
  README.md               // Project documentation
</pre>
<p>The application uses Flask routes to handle user input from web forms, validate data, and communicate with the MySQL backend for storage and calculation. Handicaps are calculated using official formula logic, with validation and logging to ensure data integrity. Future builds will expand to include modular Flask blueprints, authentication, and visual reporting.</p>

<hr>

<h2 id="collaboration">Client Collaboration</h2>
<p>Developed in collaboration with <b>active club members</b> to modernize score tracking, clarify handicap adjustments, and enhance transparency across competitive play. Regular feedback sessions guide design priorities and usability improvements. Every feature is validated through real user interaction and discussion, emphasizing clarity and reliability.</p>

<hr>

<h2 id="features">Key Features</h2>
<ul>
  <li>Player creation and record management</li>
  <li>Round score entry with validation</li>
  <li>Automated handicap calculation and updates</li>
  <li>Error handling and user feedback messages</li>
  <li>SQL data integrity enforcement for all records</li>
  <li>Version control with Git for safe iteration</li>
</ul>

<hr>

<h2 id="roadmap">Future Development Roadmap</h2>
<h3>Phase 1 – Player Experience & Transparency</h3>
<ul>
  <li>Dynamic explanations for handicap changes (“Why and How” system)</li>
  <li>Rationale messages for score adjustments or data corrections</li>
  <li>Inline help modals explaining calculation logic</li>
  <li>Improved accessibility and responsive mobile layout</li>
</ul>

<h3>Phase 2 – Tournament & Live Play</h3>
<ul>
  <li>Live tournament leaderboard with hole-by-hole updates</li>
  <li>Real-time scoring sync using Flask-SocketIO or WebSockets</li>
  <li>Mobile-friendly score entry for on-course use</li>
  <li>Group scoring mode for simultaneous player updates</li>
</ul>

<h3>Phase 3 – Analytics & Visualization</h3>
<ul>
  <li>Interactive dashboards using Chart.js or Plotly.js</li>
  <li>Player progress and trend visualizations</li>
  <li>Automatic report generation (PDF/CSV exports)</li>
  <li>Course comparison and performance summaries</li>
</ul>

<h3>Phase 4 – Cloud & Scalability</h3>
<ul>
  <li>Migrate database to AWS RDS or Google Cloud SQL</li>
  <li>Add user authentication with Flask-Login</li>
  <li>Dockerize the application for stable deployment</li>
  <li>Implement CI/CD testing via GitHub Actions</li>
</ul>

<h3>Phase 5 – Mobile App Integration</h3>
<ul>
  <li>Build companion mobile app (React Native or Flutter)</li>
  <li>Offline data entry and sync when online</li>
  <li>Push notifications for leaderboard updates</li>
  <li>Live updates and explanations mid-round</li>
</ul>

<h3>Phase 6 – Long-Term Vision</h3>
<ul>
  <li>AI-powered recommendations for skill improvement</li>
  <li>Predictive analytics for future performance</li>
  <li>Integration with wearable or GPS tracking devices</li>
</ul>

<hr>

<h2 id="about-developer">About the Developer</h2>
<p><b>Rebecca St. Clair</b><br>
🎓 <i>Computer Science Student | Aspiring Software Engineer | Writer</i><br>
A self-starter who learns by doing — building complex systems piece by piece. This project reflects not just technical growth, but persistence, curiosity, and a desire to make technology transparent and empowering for real users.</p>
<p>
  <a href="https://github.com/RebeccaStClairProjects"><img src="https://img.shields.io/badge/Portfolio-RebeccaStClairProjects-blue" alt="Portfolio Badge"></a><br>
  <a href="https://www.linkedin.com/in/rebecca-st-clair-553225236/"><img src="https://img.shields.io/badge/LinkedIn-Rebecca%20St.%20Clair-blue?logo=linkedin" alt="LinkedIn Badge"></a>
</p>

<hr>

<h2 id="license">License</h2>
<p>MIT License. See the <code>LICENSE</code> file for details.</p>
