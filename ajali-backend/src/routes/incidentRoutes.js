const express = require('express');
const router = express.Router();
const { createIncident, getIncidents } = require('../controllers/incidentController');
const authMiddleware = require('../middleware/authMiddleware');
const multer = require('multer');

// Multer config
const storage = multer.diskStorage({
  destination: (req, file, cb) => cb(null, 'uploads/'),
  filename: (req, file, cb) => cb(null, `${Date.now()}-${file.originalname}`)
});
const upload = multer({ storage });

router.post('/', authMiddleware, upload.single('media'), createIncident);
router.get('/', getIncidents);

module.exports = router;
