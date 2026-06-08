import { useState } from "react";

import UploadScreen from "./components/UploadScreen";
import Spinner from "./components/Spinner";
import AnalysisScreen from "./components/AnalysisScreen";
import EmailModal from "./components/EmailModal";

function App() {

    const [loading, setLoading] = useState(false);

    const [analysis, setAnalysis] = useState(null);

    const [showModal, setShowModal] = useState(false);

    const emailText = `Dear Client,

Thank you for your interest in our services.

Best Regards,
Team`;

    async function handleUpload() {

        setLoading(true);
        

        await new Promise((resolve) =>
            setTimeout(resolve, 3000)
        );

        setAnalysis({
            clientName: "ABC Corp",
            industry: "Information Technology",
            budget: "$100,000",
            deadline: "45 Days"
        });

        setLoading(false);
    }

    if (loading) {
        return <Spinner />;
    }

    function handleDownload() {

    alert("Downloading PDF...");
    
}

// async function handleDownload() {

//     const response =
//     await axios.get(
//         "/download-pdf",
//         {
//             responseType: "blob"
//         }
//     );

//     const url =
//     window.URL.createObjectURL(
//         response.data
//     );

//     const link =
//     document.createElement("a");

//     link.href = url;

//     link.download =
//     "report.pdf";

//     link.click();
// }


    return (

        <>

            {
                !analysis
                ?
                <UploadScreen
                    onUpload={handleUpload}
                />
                :
                <AnalysisScreen
                    analysis={analysis}
                    onDraftEmail={() =>
                        setShowModal(true)
                    }
                    onDownload={handleDownload}
                />
            }

            {
                showModal &&
                <EmailModal
                    emailText={emailText}
                    onClose={() =>
                        setShowModal(false)
                    }
                />
            }

        </>

    );
}

export default App;