$(document).ready(function() {
  var audio = $('.audio').get(0),
    textArea = $('#textArea');


  // IE and Safari not supported disabled Speak button
  if ($('body').hasClass('ie') || $('body').hasClass('safari')) {
    $('.speak-button').prop('disabled', true);
  }

  if ($('.speak-button').prop('disabled')) {
    $('.ie-speak .arrow-box').show();
  }

  $('.audio').on('error', function () {
    $('.result').hide();
    $('errorMgs').text('Sorry about this! There seems to have been an error processing your request. Please try again or contact me, at davidawad64@gmail.com');
    $('.errorMsg').css('color','red');
    $('.error').show();
  });

  $('.audio').on('loadeddata', function () {
    $('.result').show();
    $('.error').hide();
    $('#payButton').fadeIn(1600);

    $('#bookLink').fadeIn(1600);

    var audioURL = document.getElementById('AudioBook');
    $('#bookLink').attr('href', audioURL.src);

  });

  $('.download-button').click(function() {
    textArea.focus();
    if (validText(textArea.val())) {
      window.location.href = '/synthesize?download=true&' + $('form').serialize();
    }
  });

  $('.speak-button').click(function() {
    $('.result').hide();
    audio.pause();

    $('#output').typeTo("Your AudioBook Will Appear Here!");

    $('#textArea').focus();
    if (validText(textArea.val())) {
      audio.setAttribute('src','/synthesize?' + $('form').serialize());
    }
  });


  $('#payButton').hide();
  $('#bookLink').hide();
  $('#loading').hide();

});
