<script setup>


</script>

<template>
	<div class="relative py-[10%] max-w-[600px] w-full h-full mx-auto ">
		<div class="rounded-xl shadow-xl backdrop-blur-sm bg-white/60">
			<h1 class="text-4xl text-center py-8">Log in</h1>

			<form @submit.prevent="" class="block w-full px-2 md:px-4 pb-14">

				<input type="text" placeholder="Email" class="mb-8 focus:bg-white/10 border-neutral-400 focus:border-neutral-500">

				<input type="pssword" placeholder="Password" class="mb-8 focus:bg-white/10 border-neutral-400 focus:border-neutral-500">

				<button type="submit" class="btn w-full bg-gradient-to-br from-sky-400 to-indigo-400" >
					Submit
				</button>



			</form>


		</div>
	</div>

</template>