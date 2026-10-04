# Kevin Ngongang — Business Card

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![HTML](https://img.shields.io/badge/HTML-5-orange)
![CSS](https://img.shields.io/badge/CSS-3-blue)

A static, responsive landing page for `kevinpaulidor.de`, built with HTML and CSS only. It includes Kevin Ngongang's contact details, portfolio and GitHub links, and a locally stored QR code pointing to `https://www.kevinngongang.dev`.

The site has no runtime JavaScript, tracking, web fonts, or external application dependencies.

## Table of Contents
- [Features](#features)
- [Run locally](#run-locally)
- [Checks](#checks)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Clean & Minimalist Design** – A professional and visually appealing layout.  
- **Responsive Layout** – Optimized for mobile and desktop screens using CSS.  
- **Interactive Elements** – Includes hover effects for a modern user experience.  
- **QR Code Integration** – Provides quick access to the portfolio or website.  
- **Custom Styling** – Uses CSS for personalized fonts, colors, and layouts.  

## Run locally

1. **Clone the repository**:  
   ```bash
   git clone https://github.com/bakadja/business-card.git
   cd business-card
   ```  
2. **Open the project** in any code editor (VS Code, Sublime Text, etc.).  
3. **Launch the project** by opening `index.html` in a browser. 

## Checks

```bash
python3 -m unittest discover -s tests -v
```

The same checks run in GitHub Actions for every pull request. They validate the page content and links, accessibility basics, local assets, QR SVG, responsive CSS, and keyboard focus styles.

## Contributing

Contributions are welcome! To contribute:  
1. **Fork the repository**  
2. **Create a new branch** (`git checkout -b feature-branch`)  
3. **Commit your changes** (`git commit -m "Add new feature"`)  
4. **Push to the branch** (`git push origin feature-branch`)  
5. **Open a Pull Request**  

## License

This project is licensed under the **MIT License**

## Project Structure

```
business-card/
├── index.html          # Main HTML file
├── styles.css          # CSS styling
├── images/             # Directory for images and resources
│   ├── kevin.jpeg      # Profile image
│   └── qrcode.svg      # Locally generated portfolio QR code
├── tests/              # Static site checks
├── .github/workflows/  # Pull request validation
└── README.md           # Project documentation
```

---

Made with ❤️ by [Kevin](https://github.com/bakadja)
