import { useState } from "react";

import UploadScreen from "./components/UploadScreen";
import Spinner from "./components/Spinner";
import AnalysisScreen from "./components/AnalysisScreen";
import EmailModal from "./components/EmailModal";

import {
    uploadRFP,
    generateEmail,
    generateProposal
} from "./api/presalesApi";

function App() {

    const [loading, setLoading] = useState(false);

    const [analysis, setAnalysis] = useState(null);

    const [showModal, setShowModal] = useState(false);

    const [emailText, setEmailText] = useState("");

    async function handleUpload(file) {

        try {

            setLoading(true);

            const formData = new FormData();

            formData.append(
                "file",
                file
            );

            const response =
                await uploadRFP(
                    formData
                );

            setAnalysis(
                response.data
            );

        } catch (error) {

            console.error(
                "Upload Error:",
                error
            );

            alert(
                "Failed to analyze RFP."
            );

        } finally {

            setLoading(false);

        }

    }

    async function handleDraftEmail() {

        try {

            setLoading(true);

            const response =
                await generateEmail(
                    analysis,
                    "Haripriya"
                );

            setEmailText(
                response.data.body
            );

            setShowModal(true);

        } catch (error) {

            console.error(
                "Email Error:",
                error
            );

            alert(
                "Failed to generate email."
            );

        } finally {

            setLoading(false);

        }

    }

    async function handleDownload() {

        try {

            const response =
                await generateProposal(
                    analysis,
                    ""
                );

            const url =
                window.URL.createObjectURL(
                    response.data
                );

            const link =
                document.createElement(
                    "a"
                );

            link.href = url;

            link.download =
                "proposal.pdf";

            document.body.appendChild(
                link
            );

            link.click();

            link.remove();

        } catch (error) {

            console.error(
                "PDF Error:",
                error
            );

            alert(
                "Failed to download PDF."
            );

        }

    }

    if (loading) {

        return (
            <Spinner
                message="Processing..."
            />
        );

    }

    return (

        <>

            {
                !analysis
                ?
                <UploadScreen
                    onUpload={
                        handleUpload
                    }
                />
                :
                <AnalysisScreen
                    analysis={
                        analysis
                    }
                    onDraftEmail={
                        handleDraftEmail
                    }
                    onDownload={
                        handleDownload
                    }
                />
            }

            {
                showModal &&
                <EmailModal
                    emailText={
                        emailText
                    }
                    onClose={() =>
                        setShowModal(
                            false
                        )
                    }
                />
            }

        </>

    );

}

export default App;