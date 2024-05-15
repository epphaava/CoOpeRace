$(document).ready(function() {
  $('.file-row').click(function() {
      var filename = $(this).text().trim();
      fetchFileContents(filename);
  });
});

function fetchFileContents(filename) {
  fetch('/get_file_contents', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({
          filename: filename
      })
  })
  .then(response => response.text())
  .then(data => {
      // Update the content of the corresponding row with the file contents
      $('#file-contents-container').html(`<hr><h2>Contents of File: ${filename}</h2><pre>${data}</pre>`);
  });
}

$(document).ready(function() {
  $('.clickable-row').click(function() {
    var rowId = $(this).attr('data-key');
    $('#hidden-table' + rowId).toggle();
  });

  // Add click event listener to each row in the hidden table
  $('.warning-line-row').click(function() {
    var rowId = $(this).attr('data-key');
    var rowAnalyzer = $(this).attr('data-analyzer');
    console.log(rowAnalyzer)

    $('#warning-paragraph' + rowId + rowAnalyzer).toggle();

    console.log(rowId)
  });
});

