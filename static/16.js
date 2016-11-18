

$("select#children").on("change", function () {

    var number = parseInt($("#children").val());

    var label = "<div><label>Please enter information for your new entry:  </label></div>";
    var newDropList = '';
    var html = '';
    $("#childrenAge").html('');
    html += label;
    switch (number) {
        case 1:
        newDropList = '<div><label>Bag ID:  </label><input type="text" name="bid"></div><div><label>Number of items in the bag:  </label><input type="text" name="numitems"></div>';
        break;

        case 2:
        newDropList = '<div><label>Give an ID to the new item type:  </label><input type="text" name="iid"></div><div><label>Name of the new item type:  </label><input type="text" name="itemname"></div><div><label>How many of them do you want to add:  </label><input type="text" name="numofthisitem"></div><div><label>Place them in which bag (please enter bag ID):  </label><input type="text" name="bid"></div>';
        break;

        case 3:
        newDropList = '<div><label>Give this new player an ID:  </label><input type="text" name="uid"></div><div><label>Level of the player:  </label><input type="text" name="ulevel"></div><div><label>Gender:  </label><select name="gender"><option value="M">M</option><option value="F">F</option></select></div><div><label>Region:  </label><input type="text" name="regionname"></div><div><label>Team:  </label><input type="text" name="teamname"></div>';
        break;

        case 4:
        newDropList = '<div><label>Give an ID to the new pokemon:  </label><input type="text" name="pid"></div><div><label>Level:  </label><input type="text" name="plevel"></div><div><label>Which Pokemon Family does it belong to:  </label><input type="text" name="familyname"></div><div><label>Name of this Pokemon:  </label><input type="text" name="pname"></div><div><label>ID of the player who owns it:  </label><input type="text" name="uid"></div>';
        break;

        case 5:
        newDropList = '<div><label>Name of the Pokemon family:  </label><input type="text" name="familyname"></div>';
        break;

        case 6:
        newDropList = '<div><label>Name of this new region:  </label><input type="text" name="regionname"></div><div><label>How many players are in this region:  </label><input type="text" name="numplayers"></div>';
        break;

    }
    html += newDropList;

    $("#childrenAge").html(html);
});