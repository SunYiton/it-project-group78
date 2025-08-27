const express = require('express');
const app = express();

app.get('/api/health', (req, res) => {
    res.json({ status: 'ok', message: 'Server is running' });
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));