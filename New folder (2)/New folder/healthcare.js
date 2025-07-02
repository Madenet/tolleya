import React, { useState } from 'react';
import { CalendarDays, MapPin, Video, Book, Phone, Search } from 'lucide-react';

const HealthcareAccessDashboard = () => {
  const [activeTab, setActiveTab] = useState('telemedicine');
  
  // Sample data
  const doctors = [
    { id: 1, name: "Dr. Sarah Johnson", specialty: "General Practitioner", availability: "Mon, Wed, Fri", imageUrl: "/api/placeholder/150/150" },
    { id: 2, name: "Dr. Michael Chen", specialty: "Pediatrician", availability: "Tue, Thu, Sat", imageUrl: "/api/placeholder/150/150" },
    { id: 3, name: "Dr. Aisha Patel", specialty: "Cardiologist", availability: "Mon, Thu, Fri", imageUrl: "/api/placeholder/150/150" }
  ];
  
  const clinics = [
    { id: 1, name: "Community Health Center", address: "123 Main Street", services: ["General Medicine", "Pediatrics", "Vaccinations"] },
    { id: 2, name: "Women's Health Clinic", address: "456 Oak Avenue", services: ["OB/GYN", "Family Planning", "Prenatal Care"] },
    { id: 3, name: "Rural Health Post", address: "789 Country Road", services: ["Basic Care", "First Aid", "Health Education"] }
  ];
  
  const educationalResources = [
    { id: 1, title: "Understanding Diabetes", type: "Article", duration: "10 min read" },
    { id: 2, title: "Childhood Vaccination Guide", type: "Video", duration: "15 min" },
    { id: 3, title: "Maternal Health Basics", type: "Interactive Guide", duration: "20 min" }
  ];
  
  const emergencyContacts = [
    { id: 1, service: "Ambulance Service", number: "123-456-7890", available: "24/7" },
    { id: 2, service: "Poison Control", number: "098-765-4321", available: "24/7" },
    { id: 3, service: "Mental Health Crisis Line", number: "555-123-4567", available: "24/7" }
  ];

  return (
    <div className="bg-gray-50 min-h-screen p-6">
      <header className="bg-white rounded-lg shadow p-4 mb-6">
        <h1 className="text-2xl font-bold text-blue-700">Healthcare Access</h1>
        <p className="text-gray-600">Connect with healthcare providers, find resources, and manage your health</p>
      </header>
      
      {/* Navigation Tabs */}
      <div className="flex flex-wrap gap-2 mb-6">
        <button 
          onClick={() => setActiveTab('telemedicine')}
          className={`flex items-center gap-2 px-4 py-2 rounded-lg ${activeTab === 'telemedicine' ? 'bg-blue-600 text-white' : 'bg-white text-gray-700 hover:bg-gray-100'}`}
        >
          <Video size={20} />
          <span>Telemedicine</span>
        </button>
        <button 
          onClick={() => setActiveTab('clinics')}
          className={`flex items-center gap-2 px-4 py-2 rounded-lg ${activeTab === 'clinics' ? 'bg-blue-600 text-white' : 'bg-white text-gray-700 hover:bg-gray-100'}`}
        >
          <MapPin size={20} />
          <span>Find Clinics</span>
        </button>
        <button 
          onClick={() => setActiveTab('education')}
          className={`flex items-center gap-2 px-4 py-2 rounded-lg ${activeTab === 'education' ? 'bg-blue-600 text-white' : 'bg-white text-gray-700 hover:bg-gray-100'}`}
        >
          <Book size={20} />
          <span>Health Education</span>
        </button>
        <button 
          onClick={() => setActiveTab('emergency')}
          className={`flex items-center gap-2 px-4 py-2 rounded-lg ${activeTab === 'emergency' ? 'bg-blue-600 text-white' : 'bg-white text-gray-700 hover:bg-gray-100'}`}
        >
          <Phone size={20} />
          <span>Emergency</span>
        </button>
      </div>
      
      {/* Content Area */}
      <div className="bg-white rounded-lg shadow p-6">
        {activeTab === 'telemedicine' && (
          <div>
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-xl font-semibold">Virtual Consultations</h2>
              <div className="relative">
                <input 
                  type="text" 
                  placeholder="Search for doctors..." 
                  className="pl-10 pr-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <Search className="absolute left-3 top-2.5 text-gray-400" size={18} />
              </div>
            </div>
            
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
              {doctors.map(doctor => (
                <div key={doctor.id} className="border rounded-lg overflow-hidden hover:shadow-md transition-shadow">
                  <div className="flex p-4">
                    <img src={doctor.imageUrl} alt={doctor.name} className="w-16 h-16 rounded-full mr-4" />
                    <div>
                      <h3 className="font-medium">{doctor.name}</h3>
                      <p className="text-sm text-gray-600">{doctor.specialty}</p>
                      <div className="flex items-center mt-2 text-sm text-gray-500">
                        <CalendarDays size={16} className="mr-1" />
                        <span>{doctor.availability}</span>
                      </div>
                    </div>
                  </div>
                  <div className="bg-gray-50 p-3 flex justify-between">
                    <button className="text-blue-600 text-sm font-medium">View Profile</button>
                    <button className="bg-blue-600 text-white px-3 py-1 rounded-md text-sm">Book Now</button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
        
        {activeTab === 'clinics' && (
          <div>
            <h2 className="text-xl font-semibold mb-6">Find Nearby Clinics</h2>
            <div className="mb-6 p-4 border rounded-lg bg-gray-50">
              <div className="flex flex-wrap gap-4">
                <input 
                  type="text" 
                  placeholder="Enter your location" 
                  className="flex-grow px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <select className="px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
                  <option value="">All Services</option>
                  <option value="general">General Medicine</option>
                  <option value="pediatric">Pediatrics</option>
                  <option value="womens">Women's Health</option>
                </select>
                <button className="bg-blue-600 text-white px-6 py-2 rounded-lg">Search</button>
              </div>
            </div>
            
            <div className="space-y-4">
              {clinics.map(clinic => (
                <div key={clinic.id} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
                  <div className="flex justify-between">
                    <div>
                      <h3 className="font-medium">{clinic.name}</h3>
                      <p className="text-sm text-gray-600 flex items-center mt-1">
                        <MapPin size={16} className="mr-1" />
                        {clinic.address}
                      </p>
                    </div>
                    <button className="bg-blue-600 text-white px-4 py-1 h-8 rounded-md text-sm self-start">
                      Directions
                    </button>
                  </div>
                  <div className="mt-3">
                    <p className="text-sm text-gray-700 font-medium">Services:</p>
                    <div className="flex flex-wrap gap-2 mt-1">
                      {clinic.services.map((service, index) => (
                        <span key={index} className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded">
                          {service}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
        
        {activeTab === 'education' && (
          <div>
            <h2 className="text-xl font-semibold mb-6">Health Education Resources</h2>
            
            <div className="grid md:grid-cols-3 gap-6 mb-8">
              <div className="border rounded-lg p-4 bg-blue-50 text-center">
                <h3 className="font-medium mb-2">Articles</h3>
                <p className="text-sm text-gray-600 mb-4">Read in-depth health information</p>
                <button className="bg-white text-blue-600 border border-blue-600 px-4 py-2 rounded-lg text-sm font-medium">
                  Browse Articles
                </button>
              </div>
              <div className="border rounded-lg p-4 bg-green-50 text-center">
                <h3 className="font-medium mb-2">Videos</h3>
                <p className="text-sm text-gray-600 mb-4">Watch educational health videos</p>
                <button className="bg-white text-green-600 border border-green-600 px-4 py-2 rounded-lg text-sm font-medium">
                  Watch Videos
                </button>
              </div>
              <div className="border rounded-lg p-4 bg-purple-50 text-center">
                <h3 className="font-medium mb-2">Interactive Guides</h3>
                <p className="text-sm text-gray-600 mb-4">Learn through interactive content</p>
                <button className="bg-white text-purple-600 border border-purple-600 px-4 py-2 rounded-lg text-sm font-medium">
                  Explore Guides
                </button>
              </div>
            </div>
            
            <h3 className="font-medium mb-4">Popular Resources</h3>
            <div className="space-y-3">
              {educationalResources.map(resource => (
                <div key={resource.id} className="border rounded-lg p-3 flex justify-between items-center hover:bg-gray-50">
                  <div>
                    <h4 className="font-medium">{resource.title}</h4>
                    <p className="text-sm text-gray-600">
                      {resource.type} • {resource.duration}
                    </p>
                  </div>
                  <button className="text-blue-600 hover:text-blue-800">
                    View
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}
        
        {activeTab === 'emergency' && (
          <div>
            <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
              <h2 className="text-xl font-semibold text-red-700 mb-2">Emergency Resources</h2>
              <p className="text-red-600 mb-2">For life-threatening emergencies, call emergency services immediately.</p>
              <button className="bg-red-600 text-white px-6 py-2 rounded-lg font-medium">
                Call Emergency Services
              </button>
            </div>
            
            <h3 className="font-medium mb-4">Important Contact Numbers</h3>
            <div className="space-y-3 mb-6">
              {emergencyContacts.map(contact => (
                <div key={contact.id} className="border rounded-lg p-3 flex justify-between items-center">
                  <div>
                    <h4 className="font-medium">{contact.service}</h4>
                    <p className="text-sm text-gray-600">Available: {contact.available}</p>
                  </div>
                  <a 
                    href={`tel:${contact.number}`} 
                    className="bg-blue-600 text-white px-4 py-2 rounded-lg flex items-center"
                  >
                    <Phone size={16} className="mr-2" />
                    {contact.number}
                  </a>
                </div>
              ))}
            </div>
            
            <h3 className="font-medium mb-4">First Aid Resources</h3>
            <div className="grid md:grid-cols-2 gap-4">
              <div className="border rounded-lg p-3 hover:bg-gray-50">
                <h4 className="font-medium">CPR Guide</h4>
                <p className="text-sm text-gray-600 mb-2">Learn the basics of CPR</p>
                <button className="text-blue-600 text-sm font-medium">View Guide</button>
              </div>
              <div className="border rounded-lg p-3 hover:bg-gray-50">
                <h4 className="font-medium">Wound Care</h4>
                <p className="text-sm text-gray-600 mb-2">How to properly clean and dress wounds</p>
                <button className="text-blue-600 text-sm font-medium">View Guide</button>
              </div>
              <div className="border rounded-lg p-3 hover:bg-gray-50">
                <h4 className="font-medium">Choking Response</h4>
                <p className="text-sm text-gray-600 mb-2">Steps to help someone who is choking</p>
                <button className="text-blue-600 text-sm font-medium">View Guide</button>
              </div>
              <div className="border rounded-lg p-3 hover:bg-gray-50">
                <h4 className="font-medium">Recognizing Stroke</h4>
                <p className="text-sm text-gray-600 mb-2">Signs and immediate actions</p>
                <button className="text-blue-600 text-sm font-medium">View Guide</button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default HealthcareAccessDashboard;