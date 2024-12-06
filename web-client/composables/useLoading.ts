export default () => {
  const in_progress = ref(false);
  const is_error = ref(false);

  const on_load_start = () => {
    in_progress.value = false;
    is_error.value = false;
  };
  const on_error = () => {
    in_progress.value = false;
    is_error.value = true;
  };
  const on_load_end = () => {
    in_progress.value = false;
    is_error.value = false;
  };

  return {
    in_progress,
    is_error,
    on_load_start,
    on_load_end,
    on_error,
  };
};
