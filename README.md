<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
</head>
<body>

<h1>Connect 4 Game</h1>

<h2>Overview</h2>

<p>This project implements the classic game of Connect 4 using Python and the Tkinter library for the graphical user interface. It allows two players to compete against each other or a player to play against an AI opponent.</p>

<h2>Features</h2>

<ul>
  <li><strong>Two-Player Mode:</strong> Enables two human players to take turns dropping colored discs into a grid, attempting to connect four of their own discs vertically, horizontally, or diagonally.</li>
  
  <li><strong>Play Against AI:</strong> Allows a player to challenge an AI opponent that uses a simple strategy based on evaluating the game board state.</li>
</ul>

<h2>Files</h2>

<h3><code>main.py</code></h3>

<p>Contains the main logic for initiating the game. Provides a menu for selecting game modes and launching the corresponding game instances.</p>

<h3><code>two_player.py</code></h3>

<p>Defines the <code>TwoPlayerMode</code> class responsible for managing the game in two-player mode. Implements methods for handling player turns, dropping pieces, and checking for win conditions.</p>

<h3><code>play_with_ai.py</code></h3>

<p>Implements the <code>PlayWithAI</code> class for playing against an AI opponent. Includes methods for evaluating the game board state and implementing a simple AI strategy using the minimax algorithm.</p>

<h2>How to Run</h2>

<ol>
  <li><strong>Requirements:</strong>
    <ul>
      <li>Python 3.11.5</li>
      <li>Tkinter library (tk=0.1.0)</li>
      <li>Pillow library (pillow=10.1.0)</li>
    </ul>
  </li>
  <li><strong>Setup:</strong> Clone the repository to your local machine.</li>
  <li><strong>Execution:</strong> Run <code>main.py</code> using Python to start the game. Select the desired mode from the menu to play.</li>
</ol>

<h2>Usage</h2>

<p>Upon starting the game, follow the instructions on the screen to make moves. In two-player mode, take turns clicking to drop pieces into the grid. In AI mode, challenge the AI by making moves against it. The AI will then calculate and make its moves accordingly.</p>

<h2>Credits</h2>

<p>Developed by Protyay Dey. Inspired by the classic game of Connect 4.</p>

<h2>License</h2>

<p>This project is licensed under the <a href="LICENSE">MIT License</a>.</p>

</body>
</html>
