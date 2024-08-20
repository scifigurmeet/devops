# CSV 204 - Build & Release Management Lab
## Unit 3: Testing and Code Quality

### 🎯 Objectives
By the end of this practical, you will be able to:
- Use Jest to run unit tests for JavaScript/TypeScript projects
- Implement linting with ESLint
- Implement code formatting with Prettier

### 📚 Prerequisites
- Completion of Units 1 and 2
- Node.js project from previous units

### 1. Using Jest for Unit Testing

Jest is a popular testing framework for JavaScript projects. Let's set it up and write some tests.

1. Install Jest and related packages:

```bash
npm install --save-dev jest @types/jest
```

2. Update your `package.json` to include a test script:

```json
{
  ...
  "scripts": {
    "test": "jest"
  },
  ...
}
```

3. Create a new file `math.js` with some functions to test:

```javascript
function add(a, b) {
  return a + b;
}

function subtract(a, b) {
  return a - b;
}

module.exports = { add, subtract };
```

4. Create a test file `math.test.js`:

```javascript
const { add, subtract } = require('./math');

test('adds 1 + 2 to equal 3', () => {
  expect(add(1, 2)).toBe(3);
});

test('subtracts 5 - 3 to equal 2', () => {
  expect(subtract(5, 3)).toBe(2);
});
```

5. Run the tests:

```bash
npm test
```

You should see output indicating that your tests have passed.

📝 Note: Jest automatically finds and runs files with `.test.js` or `.spec.js` extensions.

### 2. Implementing Linting with ESLint

ESLint helps maintain code quality by identifying and reporting on patterns in JavaScript.

1. Install ESLint and its dependencies:

```bash
npm install --save-dev eslint
```

2. Initialize ESLint configuration:

```bash
npx eslint --init
```

Follow the prompts to set up ESLint according to your project needs. For this example, we'll choose:
- To check syntax, find problems, and enforce code style
- JavaScript modules (import/export)
- None of the frameworks
- Yes, the project uses TypeScript
- Code runs in Node
- Use a popular style guide (Airbnb)
- Config file format: JSON
- Yes, install dependencies with npm

3. This will create a `.eslintrc.json` file. Open it and add the following to the `"rules"` section:

```json
{
  ...
  "rules": {
    "semi": ["error", "always"],
    "quotes": ["error", "single"]
  }
}
```

4. Add a lint script to your `package.json`:

```json
{
  ...
  "scripts": {
    "test": "jest",
    "lint": "eslint ."
  },
  ...
}
```

5. Run the linter:

```bash
npm run lint
```

ESLint will now report any style violations in your code.

### 3. Implementing Code Formatting with Prettier

Prettier is an opinionated code formatter that ensures consistent style across your project.

1. Install Prettier and its ESLint integration:

```bash
npm install --save-dev prettier eslint-config-prettier eslint-plugin-prettier
```

2. Create a `.prettierrc` file in your project root:

```json
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5"
}
```

3. Update your `.eslintrc.json` to use Prettier:

```json
{
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "prettier"
  ],
  "plugins": ["@typescript-eslint", "prettier"],
  "rules": {
    "prettier/prettier": "error"
  }
}
```

4. Add a format script to your `package.json`:

```json
{
  ...
  "scripts": {
    "test": "jest",
    "lint": "eslint .",
    "format": "prettier --write ."
  },
  ...
}
```

5. Run the formatter:

```bash
npm run format
```

Prettier will now automatically format your code according to the rules specified in `.prettierrc`.

### 4. Integrating Everything

Now that we have testing, linting, and formatting set up, let's integrate them into our development workflow.

1. Update your `package.json` scripts to include a pre-commit hook:

```json
{
  ...
  "scripts": {
    "test": "jest",
    "lint": "eslint .",
    "format": "prettier --write .",
    "prepare": "husky install"
  },
  ...
}
```

2. Install husky and lint-staged for pre-commit hooks:

```bash
npm install --save-dev husky lint-staged
npx husky install
npx husky add .husky/pre-commit "npx lint-staged"
```

3. Add a `lint-staged` configuration to your `package.json`:

```json
{
  ...
  "lint-staged": {
    "*.js": [
      "eslint --fix",
      "prettier --write"
    ],
    "*.{json,md}": [
      "prettier --write"
    ]
  }
}
```

Now, every time you attempt to commit changes, husky will run lint-staged, which in turn will run ESLint and Prettier on your changed files.

🎉 Congratulations! You've completed Unit 3 of the Build & Release Management Lab. You've set up Jest for unit testing, ESLint for linting, and Prettier for code formatting. You've also integrated these tools into a pre-commit hook for consistent code quality.

### 📌 Key Takeaways
- Jest provides a robust framework for JavaScript unit testing.
- ESLint helps maintain code quality by enforcing coding standards.
- Prettier ensures consistent code formatting across your project.
- Integrating these tools into your workflow helps catch issues early and maintains code quality.

### 🚀 Next Steps
- Explore more advanced Jest features like mocking and snapshot testing.
- Customize ESLint rules to fit your team's coding standards.
- Investigate continuous integration tools to run these checks automatically on every push.

Remember, maintaining code quality is an ongoing process. Regularly review and update your testing and linting configurations as your project evolves.
