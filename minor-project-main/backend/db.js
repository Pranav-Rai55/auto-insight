//limMqQYzgqh3E4cw password for mongodb
const mongoose =require('mongoose')

const connectDB = async () => {
  try {
    await mongoose.connect("mongodb+srv://nakul172005_db_user:limMqQYzgqh3E4cw@cluster0.cyz57un.mongodb.net/minor_project_2");
    console.log("MongoDB connected");
  } catch (error) {
    console.error("DB connection failed:", error.message);
  }
};

module.exports = connectDB;