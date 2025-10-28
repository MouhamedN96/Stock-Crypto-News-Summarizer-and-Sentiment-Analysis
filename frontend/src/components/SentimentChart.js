import React from 'react';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

function SentimentChart({ data }) {
  if (!data || Object.keys(data).length === 0) {
    return <div>No sentiment data available</div>;
  }

  const tickers = Object.keys(data);
  const positiveData = [];
  const negativeData = [];

  tickers.forEach(ticker => {
    const sentiments = data[ticker]?.sentiments || [];
    const positive = sentiments.find(s => s.label === 'POSITIVE');
    const negative = sentiments.find(s => s.label === 'NEGATIVE');

    positiveData.push(positive ? positive.count : 0);
    negativeData.push(negative ? negative.count : 0);
  });

  const chartData = {
    labels: tickers,
    datasets: [
      {
        label: 'Positive',
        data: positiveData,
        backgroundColor: 'rgba(76, 175, 80, 0.8)',
        borderColor: 'rgba(76, 175, 80, 1)',
        borderWidth: 1,
      },
      {
        label: 'Negative',
        data: negativeData,
        backgroundColor: 'rgba(244, 67, 54, 0.8)',
        borderColor: 'rgba(244, 67, 54, 1)',
        borderWidth: 1,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: false,
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          precision: 0,
        },
      },
    },
  };

  return <Bar data={chartData} options={options} />;
}

export default SentimentChart;
