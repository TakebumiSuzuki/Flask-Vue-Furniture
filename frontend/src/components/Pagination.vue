<script setup>
  import { computed } from 'vue';

  const props = defineProps({
    totalPages: {
      type: Number,
      required: true,
    },
    currentPage: {
      type: Number,
      required: true,
    },
    // 表示するページボタンの最大数
    maxVisibleButtons: {
      type: Number,
      default: 7
    }
  });

  const emit = defineEmits(['update:currentPage']);

  // 親コンポーネントにページ変更を通知する関数
  const changePage = (page) => {
    if (page >= 1 && page <= props.totalPages && page !== props.currentPage) {
      emit('update:currentPage', page);
    }
  };

  // 表示するページ番号の配列を動的に計算。戻り値は rangeという配列
  const pages = computed(() => {
    const range = [];
    const { totalPages, currentPage, maxVisibleButtons } = props;

    if (totalPages <= maxVisibleButtons) {
      for (let i = 1; i <= totalPages; i++) {
        range.push(i);
      }
      return range;
    }

    const half = Math.floor(maxVisibleButtons / 2);
    let start = Math.max(currentPage - half, 1);
    let end = start + maxVisibleButtons - 1;

    if (end > totalPages) {
      end = totalPages;
      start = end - maxVisibleButtons + 1;
    }

    if (start > 1) {
      range.push(1);
      if (start > 2) {
        range.push('...');
      }
    }

    for (let i = start; i <= end; i++) {
      range.push(i);
    }

    if (end < totalPages) {
      if (end < totalPages - 1) {
        range.push('...');
      }
      range.push(totalPages);
    }

    return range;
  });

</script>



<template>
  <nav v-if="totalPages > 1" aria-label="Pagination">
    <ul class="flex justify-center items-center gap-3 mt-10">
      <!-- 「前へ」ボタン -->
      <li>
        <button
          @click="changePage(currentPage - 1)"
          :disabled="currentPage === 1"
          class="px-3 py-1 rounded-md transition ease-in-out"
          :class="{
            'bg-neutral-600 text-neutral-500 cursor-not-allowed': currentPage === 1,
            'bg-neutral-700 hover:bg-teal-600 text-neutral-300 cursor-pointer': currentPage !== 1
          }"
        >
          &laquo;
        </button>
      </li>

      <!-- ページ番号 -->
      <li v-for="page in pages" :key="page">

        <!-- クリック可能なページ番号 -->
        <button
          v-if="page !== '...'"
          @click="changePage(page)"
          class="px-3 py-1 rounded-md transition ease-in-out"
          :class="{
            'bg-teal-500 text-neutral-100 underline cursor-not-allowed' : page === currentPage,
            'bg-neutral-700 hover:bg-teal-600 text-neutral-300 cursor-pointer': page !== currentPage
          }"
        >
          {{ page }}
        </button>

        <!-- 省略記号 -->
        <span v-else class="px-3 py-1 text-neutral-300">
          ...
        </span>

      </li>

      <!-- 「次へ」ボタン -->
      <li>
        <button
          @click="changePage(currentPage + 1)"
          :disabled="currentPage === totalPages"
          class="px-3 py-1 rounded-md transition ease-in-out"
          :class="{
            'bg-neutral-600 text-neutral-500 cursor-not-allowed': currentPage === totalPages,
            'bg-neutral-700 hover:bg-teal-600 text-neutral-300 cursor-pointer': currentPage !== totalPages
          }"
        >
          &raquo;
        </button>
      </li>
    </ul>
  </nav>
</template>



