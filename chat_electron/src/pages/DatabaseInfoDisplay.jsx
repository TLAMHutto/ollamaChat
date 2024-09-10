import React from 'react';

const DatabaseInfoDisplay = ({ dbInfo }) => {
  if (!dbInfo) return null;

  return (
    <div className="w-full max-w-2xl mx-auto bg-white shadow-md rounded-lg overflow-hidden">
      <div className="px-6 py-4 bg-gray-100 border-b border-gray-200">
        <h2 className="text-xl font-semibold text-gray-800">Database Information</h2>
      </div>
      <div className="p-6">
        <table className="w-full">
          <thead>
            <tr className="bg-gray-50">
              <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Database Name</th>
              <th className="px-4 py-2 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Size (bytes)</th>
              <th className="px-4 py-2 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">Empty</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {dbInfo.databases.map((db) => (
              <tr key={db.name}>
                <td className="px-4 py-2 whitespace-nowrap">{db.name}</td>
                <td className="px-4 py-2 text-right whitespace-nowrap">{db.sizeOnDisk.toLocaleString()}</td>
                <td className="px-4 py-2 text-center whitespace-nowrap">{db.empty ? 'Yes' : 'No'}</td>
              </tr>
            ))}
          </tbody>
        </table>
        <div className="mt-4 text-right text-sm text-gray-600">
          <p><strong>Total Size:</strong> {dbInfo.totalSize.toLocaleString()} bytes</p>
          <p><strong>Total Size (MB):</strong> {dbInfo.totalSizeMb.toFixed(2)} MB</p>
        </div>
      </div>
    </div>
  );
};

export default DatabaseInfoDisplay;