// master/static/js/foldercon_main.js

$(function() {
  const $toggleBtn = $("#search-toggle");
  const $searchForm = $("#search-form");
  let open = false;

  $toggleBtn.on("click", function(e) {
    e.stopPropagation(); // جلوگیری از بسته شدن بلافاصله در داکیومنت کلیک
    open = !open;
    if (open) {
      $searchForm.removeClass("translate-x-full opacity-0 pointer-events-none").addClass("translate-x-0 opacity-100");
    } else {
      $searchForm.addClass("translate-x-full opacity-0 pointer-events-none").removeClass("translate-x-0 opacity-100");
    }
  });

  $(document).on("click", function(e) {
    if (!$(e.target).closest($searchForm).length && !$(e.target).closest($toggleBtn).length) {
      $searchForm.addClass("translate-x-full opacity-0 pointer-events-none").removeClass("translate-x-0 opacity-100");
      open = false;
    }
  });
});

$(document).ready(function() {
    // Function to get CSRF token from cookie (Django)
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    // Setup AJAX to send CSRF token header
    $.ajaxSetup({
        headers: { "X-CSRFToken": csrftoken }
    });

    // Open modal and fill data when clicking on warning icon
    $('[id^="warning-icon-"]').on('click', function() {
        const folderId = $(this).attr('id').split('-')[2];
        const warningTitle = $(this).data('warning-title') || '';
        const warningText = $(this).data('warning-text') || '';

        $('#report-file-id').val(folderId);
        $('#warning-title').val(warningTitle);
        $('#warning-text').val(warningText);

        $('#warning-modal').removeClass('hidden').addClass('flex');
    });

    // Close modal on clicking close button
    $('#modal-close').on('click', function() {
        $('#warning-modal').removeClass('flex').addClass('hidden');
        $('#warning-form')[0].reset();
    });

    // Close modal when clicking outside modal content
    $('#warning-modal').on('click', function(e) {
        if (e.target === this) {
            $(this).removeClass('flex').addClass('hidden');
            $('#warning-form')[0].reset();
        }
    });

    // Submit form via AJAX
    $('#warning-form').on('submit', function(e) {
    e.preventDefault();

        const warningTitle = $('#warning-title').val().trim();
        const warningText = $('#warning-text').val().trim();

        if (warningTitle === '' || warningText === '') {
            alert('Please fill in the title and text before submitting.');
            return; // ارسال فرم متوقف می‌شود
        }

        const formData = $(this).serialize();

        $.ajax({
            url: "/update-report-file/",
            method: "POST",
            data: formData,
            success: function(response) {
                alert('Your report has been submitted successfully!');
                $('#warning-modal').removeClass('flex').addClass('hidden');
                $('#warning-form')[0].reset();
            },
            error: function(xhr) {
                alert('Error submitting the report. Please try again.');
            }
        });
    });
});
