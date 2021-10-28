function processType(data) {

    // Wipe Results Tables
      try {
        $("#hitterTable > tbody").empty();
        $("#pitcherTable > tbody").empty();
      } catch (error) {
        console.error(error);
        }

  // Store roster data in object
  var roster = JSON.parse(data);

  // Verify that roster data was returned
  if (roster.player_count == 0) {
    $('#teamName').text("PICK A TEAM");
    $('#waitingNotice').text("ERROR: No Available Roster Data for Selected Team");
    return;
    }

  // Determine whether full roster or shortened roster (25 man, ideally) should be displayed
  var shortenList = true;
  if ($('#shortListDropdown :selected').val() == '0') {
    shortenList = false;
  }

  // Alert user that it's d o n e;
  $('#waitingNotice').text("Done");
  $('#teamName').text(roster.year + ' ' + roster.team_name);


  $('#hitterTable').append($('<tbody>'));
  $('#pitcherTable').append($('<tbody>'));


    // Sort players by position
  var sort_order = ['1B','2B','3B','SS','LF','CF','RF','C','IF','OF','DH','SP','RP','P','PH'];

  var players = roster.players;


  var pitchers = players.filter(function(e) {
      return ['P','SP','RP'].indexOf(e.position) >= 0;
  });


  var hitters = players.filter(function(e) {
    return pitchers.indexOf(e) < 0;
  });


  if (shortenList) {
    filtered_pitchers = pitchers.slice(0,12);

    // calculate necessary Total Plate Appearances to find lineup
    let plate_appearances = hitters.map(x => Number(x.total_plate_appearances));

    // threshold = 13th number in a list sorted numerically in descending order
    let threshold = plate_appearances.sort(function(a,b) { return a - b; }).reverse()[12];

    filtered_hitters  = hitters.filter(function(e) {
      if (isNaN(threshold)) { return true; } // If no threshold exists, just return everything
      return Number(e.total_plate_appearances) >= threshold;
      });
    players = filtered_pitchers.concat(filtered_hitters);
    }


  for (var i = 0; i < players.length; i++) {
    let current_player = players[i];
    let pitch_die = "";
    let current_table = $('#hitterTable');

    if (pitchers.indexOf(current_player) >= 0) {
        current_table = $('#pitcherTable');
        pitch_die = current_player.pitch_die;
        }

    $(current_table).append($('<tr>')
      .append($('<td scope="row">').append(current_player.jersey))
      .append($('<td>').append(current_player.full_name))
      .append($('<td>').append(current_player.position))
      .append($('<td>').append(current_player.handedness))
      .append($('<td>').append(current_player.batting_target + '/' + current_player.walk_target))
      .append($('<td>').append(current_player.traits))
      .append($('<td>').append(pitch_die))
      );
    }
  }



function fetchRoster() {
  var selectedYear = $('#yearSelectDropdown :selected').val();
  var selectedTeamID = $('#teamSelectDropdown :selected').val();
  var selectedTeamName = $('#teamSelectDropdown :selected').text();

  // AWS API for Deadball-Project
  var url = 'https://pc7bh5du32.execute-api.us-west-2.amazonaws.com/prod/retrieve?selected_year=' + selectedYear + '&selected_team=' + selectedTeamID;


  $('#waitingNotice').text("Fetching data...");

  $.getJSON(url, function(data) {
      processType(data);
    });
}

$("#submitData").click(fetchRoster);
