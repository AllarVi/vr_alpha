$(function() {
    $('a#calculate').bind('click', function() {
        $.getJSON($SCRIPT_ROOT + '/answermd5', {}, fetchAnswers);
        return false;
    });
});

setInterval(                                  //Periodically
    function()
      {
         $.getJSON(                           // Get some values from the server
            $SCRIPT_ROOT + '/answermd5',      // At this URL
            {},                               // With no extra parameters
            fetchAnswers);
      },
    2000);                                    // And do it every 2000ms

function fetchAnswers(data) {
    // Removes all previous answers
    $('.result').remove();

    // Refreshes all answers
    for (var i = 0; i < data.resultstring.length; i++) {
        console.log(data.resultstring[i])
        $('#results').append('<p class="result">' + data.resultstring[i] + '</p>');
    }
}