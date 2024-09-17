import React, { useState } from 'react';
import axios from 'axios';

const App = () => {
  const [teamInput, setTeamInput] = useState('');
  const [matchInput, setMatchInput] = useState('');
  const [rankings, setRankings] = useState([]);
  const [teamDetails, setTeamDetails] = useState(null);
  const [selectedTeam, setSelectedTeam] = useState('');
  const [selectedGroup, setSelectedGroup] = useState();
  const [updatedTeamName, setUpdatedTeamName] = useState({})
  const [updatedMatch, setUpdatedMatch] = useState({})

  const handleTeamSubmit = () => {
    const teams = teamInput.trim().split('\n').map(line => {
      const [name, registrationDate, groupNumber] = line.split(' ');
      return {
        "name": name,
        "registration_date": registrationDate,
        "group_number": groupNumber
      };
    });
    axios.post('http://127.0.0.1:3000/team', {  "data": teams })
      .then(response => {
        alert("Teams successfully submitted");
        setTeamInput("")
        })
      .catch(error => {
          alert(`Error creating teams: ${error}`);
          setTeamInput("")
      });
  };

  const handleMatchSubmit = () => {
    const matches = matchInput.trim().split('\n').map(line => {
      const [teamA, teamB, goalsA, goalsB] = line.split(' ');
      return {
          "first_team_name": teamA,
          "second_team_name": teamB,
          "first_team_score": goalsA,
          "second_team_score": goalsB
          }
    });
    axios.post('http://127.0.0.1:3000/match', { "data": matches })
      .then(response => {
        alert("Matches successfully added");
        setMatchInput("");
        }
      )
      .catch(error => {
      alert(`Error added matches: ${error}`);
      setMatchInput("")
      });
  };

  const handleUpdateTeamName = () => {
    const url = `http://127.0.0.1:3000/team?name=${updatedTeamName["oldTeamName"]}`
    axios.patch(url, {"name": updatedTeamName["newTeamName"]})
    .then(response => alert("Successfully updated team name"))
    .catch(error => alert(`Error updating team name: ${error}`))
  }

  const handleUpdateMatch = () => {
    const body = {
        "first_team_name": updatedMatch["firstTeamName"],
        "second_team_name": updatedMatch["secondTeamName"],
        "first_team_score": parseInt(updatedMatch["firstTeamScore"]),
        "second_team_score": parseInt(updatedMatch["secondTeamScore"])
    }
    axios.patch('http://127.0.0.1:3000/match', {...body})
        .then(response => {
        alert("Successfully updated team name");
        setUpdatedMatch({})
        })
        .catch(error => {
        alert(`Error updating team name: ${error}`)});
        setUpdatedMatch({})
  }

  const handleTeamDetails = () => {
    axios.get(`http://127.0.0.1:3000/team?name=${selectedTeam}`)
      .then(response => setTeamDetails(response.data.data))
      .catch(error => alert(`Error retrieving team details: ${error}`));
  };

  const handleRanking = () => {
    axios.get(`http://127.0.0.1:3000/all?group_number=${selectedGroup}`)
      .then(response => {
      setRankings(response.data.data)
      console.log(rankings)
      })
      .catch(error => alert(`Error getting rankings: ${error}`));
  };

  const handleClearData = () => {
    axios.delete('http://127.0.0.1:3000/all')
      .then(() => {
        setRankings([]);
        alert("Successfully cleared all data");
      })
      .catch(error => alert(`Error clearing data: ${error}`));
  };
  return (
    <div className="App">
      <h1>We Are The Champions</h1>

      <div>
        <h2>Enter Team Information</h2>
        <textarea
          value={teamInput}
          onChange={(e) => setTeamInput(e.target.value)}
          placeholder="Enter team data: <Team Name> <DD/MM> <Group Number>"
          rows="5"
          cols="50"
        />
        <button onClick={handleTeamSubmit}>Submit Teams</button>
      </div>

      <div>
        <h2>Enter Match Results</h2>
        <textarea
          value={matchInput}
          onChange={(e) => setMatchInput(e.target.value)}
          placeholder="Enter match results: <Team A> <Team B> <Score A> <Score B>"
          rows="5"
          cols="50"
        />
        <button onClick={handleMatchSubmit}>Submit Matches</button>
      </div>

      <div>
        <h2>Retrieve Rankings</h2>
        <input
          type="text"
          value={selectedGroup}
          onChange={(e) => setSelectedGroup(e.target.value)}
          placeholder="Enter Group Number"
        />
        <button onClick={handleRanking}>Get Rankings</button>
          {rankings && rankings.map((team, index) => (

            <li key={index}>
                {index < 4 && '[QUALIFIED] '}
                Rank {index + 1}: {team.team_name},
                Points: {team.points},
                Registration date: {team.registration_date.slice(0, team.registration_date.length - 13)}
            </li>
          ))}
      </div>

      <div>
        <h2>Retrieve Team Details</h2>
        <input
          type="text"
          value={selectedTeam}
          onChange={(e) => setSelectedTeam(e.target.value)}
          placeholder="Enter Team Name"
        />
        <button onClick={handleTeamDetails}>Get Details</button>

        {teamDetails && (
          <div>
            <h3>Team: {teamDetails["name"]}</h3>
            <p>Registration Date: {teamDetails.registration_date}</p>
            <p>Group: {teamDetails.group_number}</p>
            <p>Wins: {teamDetails.win_count}, Ties: {teamDetails.tie_count}, Losses: {teamDetails.loss_count}</p>
          </div>
        )}
      </div>

      <div>
        <h2>Update Team Name</h2>
        <input
          type="text"
          value={updatedTeamName["oldTeamName"]}
          onChange={(e) => setUpdatedTeamName({...updatedTeamName, "oldTeamName": e.target.value})}
          placeholder="Enter old team name"
        />
        <input
          type="text"
          value={updatedTeamName["newTeamName"]}
          onChange={(e) => setUpdatedTeamName({...updatedTeamName, "newTeamName": e.target.value})}
          placeholder="Enter new team name"
        />
        <button onClick={handleUpdateTeamName}>Update team name</button>
      </div>

      <div>
        <h2>Update Match</h2>
        <div>
            <input
              type="text"
              value={updatedMatch["firstTeamName"]}
              onChange={(e) => setUpdatedMatch({...updatedMatch, "firstTeamName": e.target.value})}
              placeholder="Enter 1st team name"
            />
            <input
              type="text"
              value={updatedMatch["secondTeamName"]}
              onChange={(e) => setUpdatedMatch({...updatedMatch, "secondTeamName": e.target.value})}
              placeholder="Enter 2nd team name"
            />
        </div>
        <div>
       <input
          type="text"
          value={updatedMatch["firstTeamScore"]}
          onChange={(e) => setUpdatedMatch({...updatedMatch, "firstTeamScore": e.target.value})}
          placeholder="Enter 1st team score"
        />
        <input
          type="text"
          value={updatedMatch["secondTeamScore"]}
          onChange={(e) => setUpdatedMatch({...updatedMatch, "secondTeamScore": e.target.value})}
          placeholder="Enter 2nd team score"
        />
        </div>
        <button onClick={handleUpdateMatch}>Update match</button>
      </div>

      <div>
        <h2>Clear All Data</h2>
        <button onClick={handleClearData}>Clear Data</button>
      </div>
    </div>
  );
};

export default App;
