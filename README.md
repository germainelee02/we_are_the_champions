# We Are The Champions

## Technology stack

Backend: PostgreSQL, Python, Flask

Frontend: React, JavaScript

## Instructions
1. From the `backend` sub-directory, run the command `docker-compose up`
2. From the `frontend` sub-directory, run the command `npm install`, before running `npm start`

## Assumptions
1. This annual game is happening this year (i.e. 2024)
2. Each team can only with other teams in the same group
3. Teams cannot have duplicate names, and each team is identifiable from their name, even if they change it afterwards
4. Each team cannot change group midway
5. Each team can only edit their name, and cannot edit their group number or registration date
6. When trying to edit a match, they can only change the score of each team, and not the team that participated in the match

## Design Decisions

### Database Schema

**Team**: stores all the information about a team
- Team(id, name, registration_date, group_number)
- primary key (id)

**Points**: stores the points that each team has accumulated after the matches
- Points(id, team_id, points)
- primary key (id)
- foreign key (team_id) references Team.id

**Match_Results**: stores the matches that each team has played
- Match_Results(id, first_team, second_team, first_team_score, second_team_score)
- primary key (id)
- foreign key (first_team) references (Team.id)
- foreign key (second_team) references (Team.id)

### Logical Flow

**Simultaneous updating of Points entries**
- When teams are added, a row with the corresponding team id is inserted into the Points table, with points initialised to 0
- When matches are added, the rows in Points with the corresponding team id will be automatically updated
- When matches are updated, the previous update in points will be deleted, and the new update in points will be added

**Double Match_Results entries**
- When a match results is entered, there will be two rows inserted into the table, one where \<team A> is in the column `first_team`, and another where \<team B> is in the column `first_team`
- This is to make it easier for retrieval afterwards, which will only check against the column `first_team`