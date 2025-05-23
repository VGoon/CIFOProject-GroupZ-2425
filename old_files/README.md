
 ## Wedding Seating Optimization
 The goal is to optimize the seating arrangement of guests across tables to maximize guest
 happiness and minimize conflicts based on their relationships.
 Each solution represents a complete seating arrangement, specifying which guests are
 seated at each table. These are the constraints that must be verified in every solution of the
 search space (no object is considered a solution if it doesn’t comply with these):

 - Each guest must be assigned to exactly one table.
 - Table placement matters only in terms of grouping. The arrangement within a table
 is irrelevant.

 Impossible Configurations: Any arrangement where a guest is seated at multiple tables or
 left unassigned is not part of the search space and is considered impossible. It is forbidden
 to generate such an arrangement during evolution.
 Here you can find a pairwise relationship matrix of all 64 attendees , who need to be
 distributed across 8 tables . You can also consult the chart of the guests and their
 relationships, as well as a table explaining relationship values.
 The goal is to maximize the overall relationship score by optim

### Code Requirements
For your project to be successful you must implement:
<br/> ➔ the fitness function
<br/> ➔ at least 3 mutation operators
<br/> ➔ at least 2 crossover operators
<br/> ➔ at least 2 selection mechanisms
<br/>All of these must be different from the ones implemented in class, or at least adapted to your
 chosen optimization problem, and should respect the problem’s constraints.

### Evaluation Criteria
25% Code Functionality: Assessment of the functionality of the code, the correct
 implementation of the GA techniques and interaction of the various components.
 While you will work on your projects in a group, you should ensure code is
 well-structured and works well in conjunction.
<br/>10% Code Structure: Assessment of the code quality and structure, the code should
 be clear and well-commented to be inspectable and understandable by anyone.
