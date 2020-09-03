// new
// Get Stripe publishable key
fetch("/stripe/checkout")
.then((result) => { return result.json(); })
.then((data) => {
  // Initialize Stripe.js
  const stripe = Stripe(data.publicKey);
  document.querySelector("#submitBtn").addEventListener("click", () => {
     // Get Checkout Session ID
     fetch("/stripe/checkout-session")
     .then((result) => { return result.json(); })
     .then((data) => {
     console.log(data);
     // Redirect to Stripe Checkout
     return stripe.redirectToCheckout({sessionId: data.sessionId})
     })
     .then((res) => {
     console.log(res);
     });
});
  
});
