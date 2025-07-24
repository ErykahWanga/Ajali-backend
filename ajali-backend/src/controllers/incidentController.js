const Incident = require('../models/Incident');

const createIncident = async (req, res) => {
  try {
    const { title, description, location } = req.body;
    const parsedLocation = JSON.parse(location);
    const media = req.file ? `/uploads/${req.file.filename}` : null;
    const incident = new Incident({
      title, description, location: parsedLocation, media, user: req.user.id
    });
    await incident.save();
    res.status(201).json(incident);
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: 'Server error' });
  }
};

const getIncidents = async (req, res) => {
  try {
    const { page = 1, limit = 5, search = '' } = req.query;
    const q = search
      ? { $or: [
          { title: { $regex: search, $options: 'i' } },
          { description: { $regex: search, $options: 'i' } },
          { 'location.name': { $regex: search, $options: 'i' } }
        ]}
      : {};
    const incidents = await Incident.find(q)
      .populate('user', 'username')
      .sort({ createdAt: -1 })
      .skip((+page - 1) * +limit)
      .limit(+limit);
    const total = await Incident.countDocuments(q);
    res.json({ incidents, totalPages: Math.ceil(total / limit) });
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: 'Server error' });
  }
};

module.exports = { createIncident, getIncidents };

