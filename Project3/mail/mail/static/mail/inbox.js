document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  

  // By default, load the inbox
  // When inbox is clicked, load_mailbox 
  load_mailbox('inbox');
  // compose_email('compose');

});

function load_email(id) {

  // Query to check for email first
  fetch('/emails/' + id)
        .then(response => response.json())
        .then(email => {

          // Print emails
          console.log(emails);

          // Show email
          const display = document.querySelector('#emails-view')
          display.innerHTML = `
          <div><b>From: </b> ${email['sender']}</div>
          <div><b>To: </b>${email['recipient']} </div>
          <div><b>Subject: </b>${email['subject']} </div>
          <div><b>Time: </b>${email['timestamp']} </div>
          `
  // Show emails view
  // Hide compose view
  // What does 'block' mean again?

  // Add PUT request to update the email is read or not

  // Add PUT request to update the email is archived or not

}
}

function compose_email() {

  const submit = document.querySelector('#submit');
  const bodyMessage = document.querySelector('compose-body');
  const subjectField = document.querySelector('compose-subject');
  const toField = document.querySelector('compose-recipients');
  const formSubmit = document.querySelector('form');

  // Show compose view and hide other views

  //Hides the emails-view by setting it to none
  document.querySelector('#emails-view').style.display = 'none';

  //Shows the compose-view by setting it to block
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  toField.value = '';
  subjectField.value = '';
  bodyMessage.value = '';

  // Disable submit button by default because it's blank
  submit.disabled = true;

  // Listen for input to be typed into the input field

  // If body message is empty, the submit button is disabled.
  bodyMessage.onkeyup = () => {
    if (bodyMessage.value.length > 0) {
    submit.disabled = false;
  }
  else {
    submit.disabled = true;
  }
}

  // if toField and/or Subject line is empty after submit is clicked, 
  // show pop up if user is show to send without anything

  formSubmit.onsubmit = () => {
    if (toField.value.length = 0) {
      alert('The To field is empty! Are you sure you want to continue?');
    }

    if (subjectField.value.length = 0) {
      alert('The Subject line is empty! Are you sure you want to continue?');
    }
  }
  
  // After submitting form, store the values

  formSubmit.onsubmit = () => {

    //The new submissions
    const message = bodyMessage.value;
    const subject = subjectField.value;
    const to = toField.value;

    // The magic begins here

    // Send a POST request to the URL
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: to,
        subject: subject,
        body: message,
      })
      .then(response => response.JSON())
      .then(result => {
        //Print result
        console.log(result);
      })
    });

    // Disable submit button afterwards
    submit.disabled = true;

    
    // Load sent mailbox afterwards
    load_mailbox('sent');

    // Stop form from submitting
    return false;

  }
}

  

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  // Shows emails and hides compose views 
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  

  // mailbox = inbox, sent, or archive
 
    // Query to check to see if there are any emails first
        // Send a GET request to the URL
        fetch('/emails/' + mailbox)
        .then(response => response.json())
        .then(emails => {

          // Print emails
          console.log(emails);

          emails.forEach(email => {

            // Create div element
          const elemDiv = document.createElement('div'); 

          // For each email, it gets its own div tag
          elemDiv.innerHTML = `
              <div>${email['sender']}</div>
              <div>${email['subject']} </div>
              <div>${email['timestamp']} </div>
          `;
          // Add listener to open email via ID
          elemDiv.addEventListener('click', () => load_email(id));

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

// function send