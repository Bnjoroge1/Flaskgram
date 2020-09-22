// var button = document.querySelector('#submit-button');

//     braintree.dropin.create({
//       authorization: 'server_client_token',
//       container: '#dropin-container'
//     }, function (createErr, instance) {
//       button.addEventListener('click', function () {
//         instance.requestPaymentMethod(function (err, payload) {
//           // Submit payload.nonce to your server
//         });
//       });
//     });

function myFunction(x) {
  x.classList.toggle("fa-thumbs-down");
}
window.onscroll = function() {myFunction()};

function myFunction() {
  var winScroll = document.body.scrollTop || document.documentElement.scrollTop;
  var height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
  var scrolled = (winScroll / height) * 100;
  document.getElementById("myBar").style.width = scrolled + "%";
}
$('button-follow').click(function() {
  $(this).text(function(_, text) {
    return text === "Follow" ? "Unfollow" : "Follow";
  });
  if($(this).text() == "Follow") {
    $(this).removeClass('unfollow');
  } else if($(this).text() == "Unfollow") {
    $(this).addClass('unfollow');
  }
});


  //Adding CLoudinary WIdget
const tags = ["extract", "amazing", "apple", "dog", "grass", "planes", "rocket", "rock", "movies", 
  "music", "sad", "light", "open", "mosaic", "entertainment", "test", "testament", "beach", 
  "vacation", "weather", "letter", "orchard"];

const getMyTags = (cb, prefix) => cb(prefix ? tags.filter((t) => !t.indexOf(prefix)) : tags);

var myWidget = cloudinary.createUploadWidget({
    cloudName: 'flaskgram', 
    uploadPreset: 'postupload', language: "en",  
    text: {
      "en": {
          "queue": {
              "title": "Files to upload",
              "title_uploading_with_counter": "Uploading {{num}} files"
          },
          "crop": {
              "title": "Crop your image"
  
          }
      }
    }
  , sources: ['local', 'url', 'camera', 'dropbox','facebook','google-drive','instagram']
,clientAllowedFormats: ['jpg','jpeg','png','gif'],
maxImageFileSize:150000,
maxVideoFileSize:1500000,
getTags:getMyTags
}, (error, result) => { 
      if (!error && result && result.event === "success") { 
        console.log('Done! Here is the image info: ', result.info); 
      }
    }
  )
  
document.getElementById("upload_widget").addEventListener("click", function(){
      myWidget.open();
    }, false);

const form = document.querySelector('#createPost');
    // makes POST request to store blog post on form submit
    form.onsubmit = e => {
      e.preventDefault();
      fetch("/post", {
        method: 'POST',
        body: new FormData(form)
      })
      .then(r => {
        form.reset();
      });
    } 
    