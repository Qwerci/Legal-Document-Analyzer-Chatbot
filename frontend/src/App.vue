<script setup lang="ts">
import { ref } from 'vue';
import axios from 'axios';

// State variables
const question = ref<string>('');
const answer = ref<string>('');
const summarizedContext = ref<string>('');
const searchQuery = ref<string>('');
const searchResults = ref<Array<{ document_id: number; filename: string; snippet: string }>>([]);
const file = ref<File | null>(null);
const uploadMessage = ref<string>('');
const uploadLoading = ref<boolean>(false);
const searchLoading = ref<boolean>(false);
const chatLoading = ref<boolean>(false);

// Function to ask a legal question
const askQuestion = async () => {
    if (!question.value.trim()) {
        answer.value = "Please enter a question.";
        return;
    }
    chatLoading.value = true;
    try {
        const response = await axios.get(`http://127.0.0.1:8000/api/chat/?question=${encodeURIComponent(question.value)}`);
        answer.value = response.data.answer || "No answer found.";
        summarizedContext.value = response.data.context || "";
    } catch (error) {
        console.error("Error asking question:", error);
        answer.value = "Error retrieving answer. Check console for details.";
    } finally {
        chatLoading.value = false;
    }
};

// Function to search legal documents
const searchDocuments = async () => {
    if (!searchQuery.value.trim()) {
        searchResults.value = [];
        return;
    }
    searchLoading.value = true;
    try {
        const response = await axios.get(`http://127.0.0.1:8000/api/search/?query=${encodeURIComponent(searchQuery.value)}`);
        searchResults.value = response.data.results || [];
    } catch (error) {
        console.error("Error searching documents:", error);
        searchResults.value = [];
    } finally {
        searchLoading.value = false;
    }
};

// Function to upload a legal document
const uploadFile = async () => {
    if (!file.value) {
        uploadMessage.value = "Please select a file before uploading.";
        return;
    }
    uploadLoading.value = true;
    const formData = new FormData();
    formData.append("file", file.value);

    try {
        const response = await axios.post("http://127.0.0.1:8000/api/upload/", formData, {
            headers: { "Content-Type": "multipart/form-data" },
        });
        uploadMessage.value = response.data.message || "Upload successful.";
    } catch (error) {
        console.error("Upload failed:", error);
        uploadMessage.value = "Upload failed. Check console for details.";
    } finally {
        uploadLoading.value = false;
    }
};
</script>

<template>
  <div class="app-container">
    <header class="app-header">
      <h1 class="app-title">Legal Document AI Chatbot</h1>
    </header>

    <!-- Main Content -->
    <main class="app-content">
      <!-- Upload Section -->
      <section class="app-card">
        <h2 class="card-title">Upload Legal Document</h2>
        <input type="file" @change="(e) => { const target = e.target as HTMLInputElement; if (target.files) file = target.files[0]; }" class="file-input" />
        <button class="action-button" @click="uploadFile">Upload</button>
        <p v-if="uploadMessage" class="message">{{ uploadMessage }}</p>
        <div v-if="uploadLoading" class="loading-indicator">Uploading...</div>
      </section>

      <!-- Search Section -->
      <section class="app-card">
        <h2 class="card-title">Search Legal Documents</h2>
        <input v-model="searchQuery" placeholder="Enter keyword to search" class="text-input" />
        <button class="action-button" @click="searchDocuments">Search</button>
        <ul v-if="searchResults.length" class="result-list">
          <li v-for="result in searchResults" :key="result.document_id" class="result-item">
            <strong>{{ result.filename }}</strong>: {{ result.snippet }}
          </li>
        </ul>
        <p v-if="!searchResults.length && searchQuery" class="message">No results found.</p>
        <div v-if="searchLoading" class="loading-indicator">Searching...</div>
      </section>

      <!-- Chat Section -->
      <section class="app-card">
        <h2 class="card-title">Ask Legal AI</h2>
        <input v-model="question" placeholder="Ask a legal question" class="text-input" />
        <button class="action-button" @click="askQuestion">Ask</button>
        <div v-if="chatLoading" class="loading-indicator">Thinking...</div>
        <div v-if="answer" class="response-box">
          <p class="response"><strong>Answer:</strong> {{ answer }}</p>
          <p v-if="summarizedContext" class="context"><strong>Summary Context:</strong> {{ summarizedContext }}</p>
        </div>
      </section>
    </main>
  </div>
</template>

<style scoped>
/* General Styles */
.app-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-family: 'Inter', sans-serif;
  background-color: #f9fafb;
  min-height: 100vh;
  padding: 2rem;
}

.app-header {
  text-align: center;
  margin-bottom: 2rem;
}

.app-title {
  font-size: 2rem;
  font-weight: bold;
  color: #1a1a1a;
}

.app-content {
  width: 100%;
  max-width: 800px;
}

/* Card Component */
.app-card {
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
  margin-bottom: 2rem;
  transition: transform 0.2s ease-in-out;
}

.app-card:hover {
  transform: translateY(-5px);
}

.card-title {
  font-size: 1.25rem;
  font-weight: bold;
  color: #333;
  margin-bottom: 1rem;
}

/* Input Fields */
.text-input,
.file-input {
  width: 100%;
  padding: 0.8rem;
  font-size: 1rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  margin-bottom: 1rem;
  transition: border-color 0.2s ease-in-out;
}

.text-input:focus,
.file-input:focus {
  border-color: #6366f1;
  outline: none;
}

/* Buttons */
.action-button {
  padding: 0.8rem 1.5rem;
  font-size: 1rem;
  color: #fff;
  background-color: #1e40af;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.2s ease-in-out;
}

.action-button:hover {
  background-color: #1c39bb;
}

/* Results List */
.result-list {
  list-style: none;
  padding: 0;
  margin: 0;
  color: #333;
}

.result-item {
  padding: 0.8rem;
  background: #f3f4f6;
  border-radius: 8px;
  margin-bottom: 0.5rem;
  font-size: 1rem;
}

.result-item strong {
  font-weight: bold;
  color: #1a1a1a;
  color: #333;
}

/* Messages */
.message {
  font-size: 1rem;
  color: #16a34a;
  margin-top: 0.5rem;
}

/* Loading Indicator */
.loading-indicator {
  font-size: 1rem;
  color: #6366f1;
  text-align: center;
  margin-top: 1rem;
}

/* Response Box */
.response-box {
  margin-top: 1rem;
  padding: 1rem;
  background-color: #f3f4f6;
  border-radius: 8px;
}

.response,
.context {
  font-size: 1rem;
  line-height: 1.5;
  color: #333;
}

.response strong,
.context strong {
  font-weight: bold;
  color: #1a1a1a;
}
</style>