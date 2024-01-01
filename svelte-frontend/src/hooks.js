// src/hooks.js
// export async function handle({ request, resolve }) {
// 	// Check if a theme is stored in the user's cookies
// 	const theme = request.headers.cookie?.match(/theme=(\w+);?/)?.[1] || 'light'; // Default to 'light'

// 	// Attach the theme to the request context
// 	request.locals.theme = theme;

// 	const response = await resolve(request);

// 	// Set the theme in the session
// 	if (!request.locals.session) {
// 		request.locals.session = {};
// 	}
// 	request.locals.session.theme = request.locals.theme;

// 	return response;
// }
