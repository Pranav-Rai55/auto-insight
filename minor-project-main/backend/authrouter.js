const { signup, login } = require('../controller/authcontroller.js');
const { signupValidation, loginValidation } = require('../middleware/authvalidation.js');
//import { exec }from child_process
const router = require('express').Router();

router.post('/login', loginValidation, login);
router.post('/signup', signupValidation, signup);
/**router.get("/generate", (req, res) => {
  exec("python main.py", (error) => {
    if (error) return res.status(500).send("Error generating HTML");

    // Path to the generated HTML
    const filePath = "C:\Users\nakul\OneDrive\Desktop\minor project\dashboard.html";

    res.json({ url: filePath });
  });
});*/
module.exports = router;