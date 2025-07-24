const User = require('../models/User');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');

const signup = async (req, res) => {
  try {
    console.log('signup: Request body:', req.body);

    const username = req.body.username;
    const email = req.body.email.trim().toLowerCase(); // sanitize
    const password = req.body.password;

    const existingUser = await User.findOne({ email });
    console.log('signup: Existing user check:', existingUser);
    if (existingUser) {
      return res.status(400).json({ message: 'User already exists' });
    }

    const hashedPassword = await bcrypt.hash(password, 10);
    const user = new User({ username, email, password: hashedPassword });
    console.log('signup: Saving user:', user);
    await user.save();

    const token = jwt.sign({ id: user._id }, process.env.JWT_SECRET, { expiresIn: '1h' });
    res.status(201).json({ token, user: { id: user._id, username, email } });
  } catch (err) {
    console.error('signup: Error:', err.message, err.stack);
    res.status(500).json({ message: 'Server error', error: err.message });
  }
};

const login = async (req, res) => {
  try {
    console.log('login: Request body:', req.body);

    const email = req.body.email.trim().toLowerCase(); // sanitize
    const password = req.body.password.trim();

    const user = await User.findOne({ email });
    console.log('login: User found:', user);
    if (!user) {
      return res.status(400).json({ message: 'Invalid credentials' });
    }

    const isMatch = await bcrypt.compare(password, user.password);
    console.log('login: Password match:', isMatch);
    if (!isMatch) {
      return res.status(400).json({ message: 'Invalid credentials' });
    }

    const token = jwt.sign({ id: user._id }, process.env.JWT_SECRET, { expiresIn: '1h' });
    res.json({ token, user: { id: user._id, username: user.username, email } });
  } catch (err) {
    console.error('login: Error:', err.message, err.stack);
    res.status(500).json({ message: 'Server error', error: err.message });
  }
};

module.exports = { signup, login };
