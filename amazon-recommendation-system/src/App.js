import React, { Component } from 'react';
import axios from "axios";

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      categories: [

      ],
      selectedCategory: '',
      purchasedProducts: [

      ],
      recommendation: [

      ]
    };
  }

  handleChange = (event) => {
    this.setState({ selectedCategory: event.target.value });
  };

  handleButtonClick = () => {
    axios
      .post(
        "http://localhost:8000/user/predict",
        { user_id: this.state.selectedCategory }
      )
      .then((response) => {
        console.log(response.data);
        if (response.status === 200) {
          console.log(response.data.purchased);
          this.setState({ purchasedProducts: response.data.purchased, recommendation: response.data.prediction });
        }
      })
      .catch((error) => {
        console.error("There was an error!", error);
      });
  };

  componentDidMount() {
    axios
      .get(
        "http://localhost:8000/user/get_user_id"
      )
      .then((response) => {
        console.log(response.data);
        if (response.status === 200) {
          this.setState({ categories: response.data.random_user_ids });
        }
      })
      .catch((error) => {
        console.error("There was an error!", error);
      });
  }

  render() {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-slate-950 to-black text-white flex flex-col items-center justify-start space-y-12 px-6 pt-12 pb-24">

        {/* Header Section */}
        <div className="text-center p-10 rounded-2xl shadow-2xl bg-white/10 backdrop-blur-md border border-sky-900 max-w-4xl w-full">
          <h1 className="text-4xl sm:text-6xl font-bold text-white tracking-tight drop-shadow-xl">
            Amazon Product Recommendation
          </h1>
          <p className="mt-4 text-lg sm:text-xl text-sky-200 font-medium">
            Discover your next favorite product – smart, fast, and personalized.
          </p>
        </div>

        {/* Category Dropdown and Button */}
        <div className="w-full max-w-2xl bg-sky-950 bg-opacity-30 p-6 rounded-2xl shadow-xl border border-sky-800 flex flex-col sm:flex-row items-center gap-4">
          <p className="mb-1 text-lg sm:text-xl text-sky-200 font-medium">
            User ID
          </p>
          <select
            id="category"
            className="flex-grow p-3 rounded-lg bg-gray-800 text-white border border-sky-700 focus:outline-none focus:ring-2 focus:ring-sky-400 transition-all"
            value={this.state.selectedCategory}
            onChange={this.handleChange}
          >
            <option value="" disabled>Select a category</option>
            {this.state.categories.map((category, index) => (
              <option key={index} value={category}>{category}</option>
            ))}
          </select>

          <button
            onClick={this.handleButtonClick}
            className="px-6 py-3 bg-sky-600 hover:bg-sky-700 active:bg-sky-800 rounded-lg shadow-md text-white font-semibold transition duration-300"
          >
            Recommend
          </button>
        </div>

        {/* Tables Section */}
        <div className="w-full max-w-6xl grid md:grid-cols-2 gap-10">

          {/* Purchased Products Table */}
          <div className="bg-sky-950 bg-opacity-30 rounded-2xl shadow-lg border border-sky-800 max-h-80 overflow-y-auto">
            <h2 className="text-2xl font-semibold text-sky-200 border-b border-sky-700 p-4 sticky top-0 bg-sky-950 bg-opacity-70 z-20 backdrop-blur-md">
              Purchased Products
            </h2>
            <table className="min-w-full text-left text-white">
              <thead className="sticky top-[3.5rem] bg-sky-950 bg-opacity-70 border-b border-sky-700 z-10 backdrop-blur-md">
                <tr>
                  <th className="py-3 px-5 text-lg font-medium">Name</th>
                </tr>
              </thead>
              <tbody>
                {this.state.purchasedProducts.length > 0 ? (

                  this.state.purchasedProducts.map((product, index) => (
                    <tr
                      key={index}
                      className={`border-b border-sky-800 hover:bg-sky-900/40 transition-all ${index % 2 === 0 ? 'bg-sky-900/30' : ''}`}
                    >
                      <td className="py-3 px-5">{product}</td>
                    </tr>
                  ))) : (<tr>
                    <td
                      colSpan="2"
                      className="px-6 py-4 text-center text-gray-500 dark:text-gray-400"
                    >
                      No Data Available
                    </td>
                  </tr>)}
              </tbody>
            </table>
          </div>

          {/* Expected Ratings Table */}
          <div className="bg-sky-950 bg-opacity-30 rounded-2xl shadow-lg border border-sky-800 max-h-80 overflow-y-auto">
            <h2 className="text-2xl font-semibold text-sky-200 border-b border-sky-700 p-4 sticky top-0 bg-sky-950 bg-opacity-70 z-20 backdrop-blur-md">
              Recommendations
            </h2>
            <table className="min-w-full text-left text-white">
              <thead className="sticky top-[3.5rem] bg-sky-950 bg-opacity-70 border-b border-sky-700 z-10 backdrop-blur-md">
                <tr>
                  <th className="py-3 px-5 text-lg font-medium">Product Name</th>
                  <th className="py-3 px-5 text-lg font-medium">Expected Rating</th>
                </tr>
              </thead>
              <tbody>
                {this.state.purchasedProducts.length > 0 ? (
                  this.state.recommendation.map((item, index) => (
                    <tr
                      key={index}
                      className={`border-b border-sky-800 hover:bg-sky-900/40 transition-all ${index % 2 === 0 ? 'bg-sky-900/30' : ''}`}
                    >
                      <td className="py-3 px-5">{item.productName}</td>
                      <td className="py-3 px-5">{item.expectedRating.toFixed(1)}</td>
                    </tr>
                  ))) : (<tr>
                    <td
                      colSpan="2"
                      className="px-6 py-4 text-center text-gray-500 dark:text-gray-400"
                    >
                      No Data Available
                    </td>
                  </tr>)}
              </tbody>
            </table>
          </div>

        </div>
      </div>
    );
  }
}

export default App;
