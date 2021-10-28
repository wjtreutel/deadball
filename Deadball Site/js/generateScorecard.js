// A $( document ).ready() block.
$( document ).ready(function() {
    console.log( "ready!" );

    createBoxScoreTable();
});

function createBoxScoreTable() {
  let rowHeaders = ["A:","H:"];
  for (let i=0; i < rowHeaders.length; i++) {
    let newRow = $('<tr>')
                  .append($('<td scope="row">').append(rowHeaders[i]));

    for (let j = 0; j < 15; j++) {
      newRow.append($('<td>'));
        }

    $('#boxScoreTable').append(newRow);
  }
}

function createScoreCardTable(teamData,targetTable) {
  for (let i = 0; i < 8; i++) {
    let newRow = $('<tr>').append($('<td scope="row">').append(teamData.players[i].full_name));

    newRow.append($('<td>').append(teamData.players[i].position));
    newRow.append($('<td>').append(teamData.players[i].handedness.toUpperCase()));
    newRow.append($('<td>').append(teamData.players[i].batting_target));
    newRow.append($('<td>').append(teamData.players[i].walk_target));
    newRow.append($('<td class="wideCell rightBorder">').append(teamData.players[i].traits));

    for (let j = 0; j < 12; j++) {
      newRow.append($('<td class="wideCell">'));
    }

    targetTable.append(newRow);
  }
  let newRow = $('<tr class="PitcherRow">').append($('<td scope="row">'));


  for (let j = 0; j < 17; j++) {
    let cellHTML = "<td>";
    if (j == 4) { cellHTML = "<td class='rightBorder'>"; }
    newRow.append($(cellHTML));
  }

targetTable.append(newRow);
}



function createHitterTable(teamData) {

  for (let i = 0; i < 13; i++) {
    let newRow = $('<tr>').append($('<td scope="row">').append(i + 1));

    newRow.append($('<td>').append(teamData.players[i].full_name));
    newRow.append($('<td>').append(teamData.players[i].position));
    newRow.append($('<td>').append(teamData.players[i].handedness.toUpperCase()));
    newRow.append($('<td>').append(teamData.players[i].batting_target));
    newRow.append($('<td>').append(teamData.players[i].walk_target));
    newRow.append($('<td class="wideCell">').append(teamData.players[i].traits));

    $('#hitterTable').append(newRow);
  }
}


function createPitcherTable(teamData) {


    for (let i = 13; i < 25; i++) {
      let newRow = $('<tr>').append($('<td scope="row">').append(teamData.players[i].position));

      newRow.append($('<td>').append(teamData.players[i].full_name));
      newRow.append($('<td>').append(teamData.players[i].pitch_die));
      newRow.append($('<td>').append(teamData.players[i].handedness));
      newRow.append($('<td>').append(teamData.players[i].batting_target));
      newRow.append($('<td>').append(teamData.players[i].walk_target));
      newRow.append($('<td class="wideCell">').append(teamData.players[i].traits));


    $('#pitcherTable').append(newRow);
  }
}




// Submit API Request
function fetchRoster() {
  //var selectedYear = $('#yearSelectDropdown :selected').val();
  var selectedTeamID = $('#teamSelectDropdown :selected').val();
  //var selectedTeamName = $('#teamSelectDropdown :selected').text();

  var selectedYear = "2019";

  // AWS API for Deadball-Project
  var url = 'https://pc7bh5du32.execute-api.us-west-2.amazonaws.com/prod/query?selected_year=' + selectedYear + '&selected_team=' + selectedTeamID;


  $('#waitingNotice').text("Fetching data...");

  $.getJSON(url, function(data) {
      processType(data);
    });
}

$("#submitData").click(fetchRoster);

function processType(data) {
  // Store roster data in object
  var roster = JSON.parse(data);


  $('.teamHeader').text(roster.team_name.toUpperCase());
  try {
    $(".scorecardTable > tbody").empty();
    $("#hitterTable > tbody").empty();
    $("#pitcherTable > tbody").empty();
  } catch (error) {
    console.error(error);
    }

  createScoreCardTable(roster,$('.scorecardTable'));
  createHitterTable(roster);
  createPitcherTable(roster);
}
