// Importing express package
const express = require("express");
// Importing isomorphic-fetch package
const fetch = require("isomorphic-fetch");

// instantiating express package
const app = express();

// Making public folder static where index.html file is present
// By making it static, we can easily serve index.html page
app.use(express.static("public"));

// To accept HTML form data
app.use(express.urlencoded({ extended: false }));

// Here, HTML form is submit
app.post("/submit", (req, res) => {
const name = req.body.name;
// getting site key from client side
const response_key = req.body["g-recaptcha-response"];
// Put secret key here, which we get from google console
const secret_key = "6LfFDwUTAAAAAIyC8IeC3aGLqVpvrB6ZpkfmAibj";

// Hitting POST request to the URL, Google will
// respond with success or error scenario.
const url =
`https://www.google.com/recaptcha/api/siteverify?secret=${secret_key}&response=${response_key}`;

// Making POST request to verify captcha
fetch(url, {
	method: "post",
})
	.then((response) => response.json())
	.then((google_response) => {

	// google_response is the object return by
	// google as a response
	if (google_response.success == true) {
		// if captcha is verified
		return res.send({ response: "Successful" });
	} else {
		// if captcha is not verified
		return res.send({ response: "Failed" });
	}
	})
	.catch((error) => {
		// Some error while verify captcha
	return res.json({ error });
	});
});

// lifting the app on port 4000.
const PORT = 4000;
app.listen(PORT, () => console.log(`Server is running on PORT ${PORT}`));
