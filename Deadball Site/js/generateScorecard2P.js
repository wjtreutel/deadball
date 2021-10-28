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
      newRow.append($('<td>').append(''));
        }

    $('#boxScoreTable').append(newRow);
  }
}


function createScoreCardTable(teamData,targetTable) {
  for (let i = 0; i < 8; i++) {
    let newRow = $('<tr>').append($('<td scope="row">').append(teamData.players[i].full_name));

    newRow.append($('<td>').append(teamData.players[i].position.toUpperCase()));
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



// Submit API Request
function fetchRoster() {
  //var selectedYear = $('#yearSelectDropdown :selected').val();
  var selectedHomeTeam = $('#homeSelectDropdown :selected').val();
  var selectedAwayTeam = $('#awaySelectDropdown :selected').val();
  //var selectedTeamName = $('#teamSelectDropdown :selected').text();


    try {
      $(".awayTeam > tbody").empty();
      $(".homeTeam > tbody").empty();
    } catch (error) {
      console.error(error);
      }

  var selectedYear = "2019";

  // AWS API for Deadball-Project
  var url_home = 'https://pc7bh5du32.execute-api.us-west-2.amazonaws.com/prod/query?selected_year=' + selectedYear + '&selected_team=' + selectedHomeTeam;
  var url_away = 'https://pc7bh5du32.execute-api.us-west-2.amazonaws.com/prod/query?selected_year=' + selectedYear + '&selected_team=' + selectedAwayTeam;

  $('#waitingNotice').text("Fetching data...");

    $.getJSON(url_away,function(data) {
      let text = $('#awaySelectDropdown :selected').text().toUpperCase();
      $('.awayLabel').text(text);
      processType(data,$('.awayTeam'));
    });

  $.getJSON(url_home, function(data) {
    let text = $('#homeSelectDropdown :selected').text().toUpperCase();
    $('.homeLabel').text(text);
      processType(data,$('.homeTeam'));
      $('.scorecardContainer').show();
    });
}

$("#submitData").click(fetchRoster);

function processType(data,targetTable) {
  // Store roster data in object
  var roster = JSON.parse(data);

  createScoreCardTable(roster,targetTable);
}
