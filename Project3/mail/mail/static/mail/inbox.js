document.addEventListener('DOMContentLoaded', function () {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

  // Submit form function
  document.querySelector('#compose-form').onsubmit = submit_email;

  // Disable submit button by default because it's blank
  document.querySelector('#submit').disabled = true;

  // Listen for input in body message
  let bodyMessage = document.querySelector('#compose-body');
  bodyMessage.onkeyup = () => {
    if (bodyMessage.value.length > 0) {
      submit.disabled = false;
    }
    else {
      submit.disabled = true;
    }
  }

});

/*
When loading email via its ID, it queries first before showing the emails view and hiding the compose view
If the email is read, it will show the 'Mark as Unread' button. Otherwise, shows 'Mark as Read'.
When 'Reply' is clicked, it will pre-fill the compose-view and emails-view. 
If the email is not archive, it will show the 'Archive' button. Otherwise, shows 'Unarchive'. 
Once archived/unarchived, load the user's inbox.
*/

function load_email(id) {

  // Show emails view and hide compose view
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Query to check for email first
  fetch('/emails/' + id)
    .then(response => response.json())
    .then(email => {

      // Show email
      const display = document.querySelector('#emails-view');
      display.innerHTML = `
          <div><b>From: </b> ${email['sender']}</div>
          <div><b>To: </b>${email['recipient']} </div>
          <div><b>Subject: </b>${email['subject']} </div>
          <div><b>Time: </b>${email['timestamp']} </div>
          <div><b>Body: </b>${email['body']}</div>
          `;

      // Add PUT request to update the email is read
      fetch('/emails/' + id, {
        method: 'PUT',
        body: JSON.stringify({
          read: true
        })
      })

      // Add reply button here and pre-fill the innerhtml
      replyButton = document.createElement('button');
      replyButton.innerHTML = "Reply";
      replyButton.addEventListener('click', function () {
        compose_email();

        // Hide emails view and show compose-view
        document.querySelector('#emails-view').style.display = 'none';
        document.querySelector('#compose-view').style.display = 'block';

        // Pre-fill the recipients in To field
        document.querySelector('#compose-recipients').value = email.sender;

        // Pre-fill subject line
        // If it already has Re then don't add another one
        let checkSubject = email.subject;
        if (!checkSubject.includes("Re:", 0)) {
          let re = `
        Re: ${email['subject']}
        `
          document.querySelector('#compose-subject').value = re;
        } else {
          document.querySelector('#compose-subject').value = checkSubject;
        }

        // Pre-fill the body
        // With a "On Jan 1 2020, 12:00 AM foo@example.com wrote:" followed by the original text of the email.
        let body = `
      On ${email['timestamp']}, ${email['sender']} wrote:
      `
        document.querySelector('#compose-body').value = body;

      })
      // });
      display.appendChild(replyButton);

      // Create Mark Unread Button
      // If email read is true, show mark unread button
      // Then go to inbox after

      markUnread = document.createElement('button');
      markUnread.innerHTML = "Mark as Unread";
      markUnread.addEventListener('click', function () {
        // Add PUT request to update the email is false
        fetch('/emails/' + id, {
          method: 'PUT',
          body: JSON.stringify({
            read: false
          })
            .then(response => load_mailbox('inbox'))
        })

        display.appendChild(markUnread);

        // Create Archive button
        // Only applies to 'Inbox' and 'Archive' mailboxes. Not 'Sent'. 
        // After archive/unarchive, go to inbox
        markArchive = document.createElement('button');
        markArchive.innerHTML = "Archive";
        markArchive.addEventListener('click', function () {
          // Add PUT request to update the email is archived or not
          fetch('/emails/' + id, {
            method: 'PUT',
            body: JSON.stringify({
              archived: true
            })
              .then(response => load_mailbox('inbox'))
          })
          display.appendChild(markArchive);
        })
      })
    })
}
/*
When composing new mail, hide the emails view to show the compose view and set all fields to empty
Checks that email is not empty by disabling the submit button
If To field and Subject line is empty, it will show a dialog box
Send POST request once everything is filled out
*/
function compose_email() {
  // Hide emails view and show compose view
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

/* 
 If toField and/or Subject line is empty after submit is clicked, 
 show pop up if user is show to send without anything
 */

function validate_fields() {

  const subjectField = document.querySelector('#compose-subject').value;
  const toField = document.querySelector('#compose-recipients').value;

    if (toField.length == 0) {
      alert('You forgot to put in the recipient\'s email address!');
      return false;
    };

    if (subjectField.length == 0) {
      if (confirm('The Subject line is empty! Are you sure you want to continue?')) {
        submit_email(); 
      } else {
          return false;
        }
      }
    };

function submit_email() {

  const submit = document.querySelector('#submit');
  const bodyMessage = document.querySelector('#compose-body').value;
  const subjectField = document.querySelector('#compose-subject').value;
  const toField = document.querySelector('#compose-recipients').value;

    // Send a POST request to the URL
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: toField,
        subject: subjectField,
        body: bodyMessage,
      })
    })
        .then(response => response.json())
        .then(result => {
          //Print result
          console.log(result);

          // Load sent mailbox afterwards
          load_mailbox('sent');
    })

    // Disable submit button afterwards
    submit.disabled = true;

    // Stop form from submitting
    return false;
  // })
}


/*
When loading the mailbox, it will list out all the emails as its on line
If unread, it's bold with white background
If read, it's not bold with gray background
*/


function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  // Shows emails and hides compose views 
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';


  // Query to check to see if there are any emails first
  // Send a GET request to the URL
  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {

      // Print emails
      console.log(emails);

      emails.forEach(email => {

        // Create div element
        const elemDiv = document.createElement('div');

        // For each email, it gets its own div tag.. for now
        elemDiv.innerHTML = `
              <div>${email['sender']} <span class="timestamp">${email['subject']} ${email['timestamp']} </span> </div>
              
          `;

        // Change color if email is read or not
        // if unread then all divs are bold

        if (email.read) {
          elemDiv.classList.add('email-read');
        } else {
          elemDiv.classList.add('email-unread');
        }

        // Add listener to open email via ID
        elemDiv.addEventListener('click', () => load_email(email.id));

        // Append to DOM
        document.querySelector('#emails-view').appendChild(elemDiv);

      })
    })

  // Show the mailbox name
  // Displays the name of the selected mailbox
  // Capitalizes the first letter
  // slice - used to extract a portion of an array into a new array object
  // slice begins at 1
  // I + nbox = Inbox
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

};