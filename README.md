
 1. Wedding Seating Optimization
 The goal is to optimize the seating arrangement of guests across tables to maximize guest
 happiness and minimize conflicts based on their relationships.
 Each solution represents a complete seating arrangement, specifying which guests are
 seated at each table. These are the constraints that must be verified in every solution of the
 search space (no object is considered a solution if it doesn’t comply with these):

 Each guest must be assigned to exactly one table.

 Table placement matters only in terms of grouping. The arrangement within a table
 is irrelevant .
 Impossible Configurations: Any arrangement where a guest is seated at multiple tables or
 left unassigned is not part of the search space and is considered impossible. It is forbidden
 to generate such an arrangement during evolution.
 Here you can find a pairwise relationship matrix of all 64 attendees , who need to be
 distributed across 8 tables . You can also consult the chart of the guests and their
 relationships, as well as a table explaining relationship values.
 The goal is to maximize the overall relationship score by optim