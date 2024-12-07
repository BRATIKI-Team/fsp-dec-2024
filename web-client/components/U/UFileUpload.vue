<script setup lang="ts">
import { ref, watch, defineProps, defineEmits } from 'vue';

interface UploadedFile {
  id: string;
  name: string;
  file?: File;
  uploading: boolean;
  error?: boolean;
}

const props = defineProps({
  modelValue: {
    type: Array as () => { id: string; name: string }[],
    default: () => [],
  },
  multiple: {
    type: Boolean,
    default: true
  }
});

const emit = defineEmits(['update:modelValue']);

const uploadedFiles = ref<UploadedFile[]>([]);
const isDragging = ref(false);

const handleDragOver = (event: DragEvent) => {
  event.preventDefault();
  isDragging.value = true;
};

const handleDragLeave = () => {
  isDragging.value = false;
};

const handleDrop = (event: DragEvent) => {
  event.preventDefault();
  isDragging.value = false;
  if (event.dataTransfer?.files) {
    handleFiles(Array.from(event.dataTransfer.files));
  }
};

const handleFiles = async (files: File[]) => {
  files.forEach(file => {
    const newFile: UploadedFile = {
      id: '',
      name: file.name,
      file,
      uploading: true,
    };
    uploadedFiles.value = [...uploadedFiles.value, newFile];
    uploadFile(newFile, uploadedFiles.value.length - 1);
  });
};

const uploadFile = async (file: UploadedFile, idx: number) => {
  if (file.file == undefined) {
    return;
  }

  const formData = new FormData();
  formData.append('file', file.file);

  try {
    const response = await fetch('http://localhost:8000/files/upload', {
      method: 'POST',
      body: formData,
    });

    if (response.ok) {
      const result = await response.text();
      file.id = result.replaceAll("\"", "");
      file.name = file.file.name;
      file.uploading = false;
      uploadedFiles.value[idx] = { ...file };
      updateModelValue();
    } else {
      console.error('Upload failed');
    }
  } catch (error) {
    console.error('Error uploading file:', error);
    file.uploading = false;
    file.error = true;
    uploadedFiles.value[idx] = { ...file };
  }
};

const removeFile = (id: string) => {
  uploadedFiles.value = uploadedFiles.value.filter(file => file.id !== id);
  updateModelValue();
};

const updateModelValue = () => {
  const simplifiedFiles = uploadedFiles.value
    .filter(file => file.id) // Only include files that have been successfully uploaded
    .map(file => ({ id: file.id, name: file.name }));
  emit('update:modelValue', simplifiedFiles);
};

// Watch for external changes to modelValue
watch(
  () => props.modelValue,
  (newValue) => {
      const valsToAdd: UploadedFile[] = []
      newValue.map(file => {
          if (uploadedFiles.value.findIndex(i => i.id == file.id) < 0) {
            valsToAdd.push({
              id: file.id,
              name: file.name,
              uploading: false
            })
          }
      });

      uploadedFiles.value.push(...valsToAdd)
  },
  { immediate: true }
);
const uploadedFilesOnly = computed(() => uploadedFiles.value.filter(i => !i.error))
</script>

<template>
  <div
    class="border-2 border-dashed rounded-md text-center p-6 cursor-pointer mb-4"
    :class="{ 'is-dragging': isDragging }"
    @dragover="handleDragOver"
    @dragleave="handleDragLeave"
    @drop="handleDrop"
    @click="$refs.fileInput.click()"
  >
    <UIcon name="i-heroicons-document-arrow-down" class="w-10 h-10"/>
    <p >Переместите файлы сюда или <b>кликните для загрузки</b></p>
    <input type="file" ref="fileInput" :multiple="props.multiple" @change="(e) => handleFiles(Array.from(e.target.files))" hidden />
  </div>

  <div class="uploaded-files">
    <div v-for="file in uploadedFilesOnly" :key="file.id" class="file-item">
      <div class="bg-elevated text-dimmed border border-dimmed rounded md px-4 py-2 flex items-center justify-between mb-4">
        <span>{{ file.name }}</span>
        <div class="flex items-center">
          <UProgress v-if="file.uploading" animation="carousel" class="mr-2"/>
          <button @click="removeFile(file.id)">✖</button>
        </div>
      </div>
    </div>
  </div>
</template>
