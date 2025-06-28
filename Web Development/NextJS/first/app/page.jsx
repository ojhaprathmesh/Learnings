"use client";
import { useState, useEffect } from "react";

export default function Home() {
  const [count, setCount] = useState(0);
  console.log("Home component rendered");
  return (
    <div>
      <div>You are at Home Page</div>
      <div className="text-2xl">Count: {count}
        <button
          className="ml-4 bg-blue-500 text-white px-4 py-2 rounded"
          onClick={() => setCount(count + 1)}
        >
          Increment
        </button>
      </div>
    </div>
  );
}
