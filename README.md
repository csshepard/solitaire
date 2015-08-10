Solitaire
=======
A simple text based Solitaire game played with keyboard input

Start game with "python main.py"

- The following inputs are valid:
  - 1 or <blank>: Draws a card from the deck
  - 2: Moves card(s) from one pile to another
  - 3: Automatically moves all valid cards to the foundation piles
  - 4: Undo the last move
  - 5: Start a new game
  - 0: Quit current game
- When moving a card the following inputs are used to specify a pile  
  - 0: Draw Pile
  - 1-7: The Tableau Piles from left to right
  - H: The Foundation Piles (used when moving to foundation piles)
  - H1-H4: The Foundation Piles from left to right (used when moving from the foundation piles)

The four foundation piles always hold the same suit.  From left to right they are Spade, Heart, Club, Diamond.

Inputs for a single move can be chained.  Examples:
- "2 0 1" will attempt to move a card from the draw pile to the first tableau pile.
- "2 2 7" will attempt to move cards from the second tableau pile to the seventh.
- "2 3 H" will attempt to move a card from the third tableau pile to the appropriate foundation pile.
- "2 H1 1" will attempt to move a card from the first foundation pile to the first tableau pile.
