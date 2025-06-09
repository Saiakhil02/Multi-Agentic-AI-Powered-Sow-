import { useRef, useState, useEffect } from "react";
import axios from "axios";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import MarkdownPreview from '@uiw/react-markdown-preview';
import { Card } from "@/components/ui/card";
import { Loader2, Download, ThumbsUp, ThumbsDown } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { ResizablePanelGroup, ResizablePanel, ResizableHandle } from "@/components/ui/resizable";
import { Label } from "@/components/ui/label";
import { ScrollArea } from "@/components/ui/scroll-area";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Export2Word } from "./exportToWord";

const API_BASE_URL = 'http://127.0.0.1:8080'

interface SOWFormData {
  sowType: string;
  workType: string;
  projectObjectives: string;
  projectScope: string;
  servicesDescription: string;
  specificFeatures: string;
  platformsTechnologies: string;
  integrations: string;
  designSpecifications: string;
  outOfScope: string;
  deliverables: string;
  timeline: string;
}

const defaultValues = {
  sowType: "fixed",
  workType: "discovery",
  projectObjectives:  `The Client operates a complex on-premise environment, primarily leveraging Microsoft SQL Server for multiple transactional systems, both homegrown and commercial. These systems encompass transportation management, order management, finished vehicle tracking, inspections, and claims processing. While these systems generate substantial data volumes, they offer limited analytical and reporting capabilities. Currently, different departments rely on a centralized BI function for ad-hoc reporting, which creates bottlenecks in data access and strains the transactional databases`,
  projectScope: `The Discovery and Assessment phase will be considered complete upon delivery and acceptance of:
5.1.	All documented deliverables outlined in Section 3
5.2.	Final presentation of findings and recommendations
5.3.	Proposed implementation roadmap
`,
  servicesDescription: `HeapSync will provide the following Services: 
2.1.	Stakeholder Engagement and Current State Analysis A thorough review of existing systems and processes through structured interviews and documentation review.
2.2.	Technical Evaluation Detailed assessment of current architecture, system capabilities, and integration points.
2.3.	Gap Analysis and Recommendations Comprehensive analysis of current state versus industry best practices, leading to actionable recommendations.
2.4.	Implementation Planning Development of a strategic roadmap for modernizing the data platform environment.
`,
  specificFeatures: `The Discovery and Assessment phase will be considered complete upon delivery and acceptance of:
5.1.	All documented deliverables outlined in Section 3
5.2.	Final presentation of findings and recommendations
5.3.	Proposed implementation roadmap
`,
  platformsTechnologies: "",
  integrations: "",
  designSpecifications: "",
  outOfScope: `As a condition for recovery of any liability, the parties must assert any claim under this SOW within three (3) months after discovery or sixty (60) days after the termination or expiration of this SOW, whichever is earlier. In no event will either party to this Agreement be liable for incidental, consequential, punitive, indirect or special damages, including, without limitation, interruption or loss of business, profit or goodwill.  In no event shall HeapSync's liability to Client exceed the fees received from Client under this SOW during the six (6) month period preceding the claim to which the liability relates, whether arising from an alleged breach of the Agreement or this SOW, an alleged tort, or any other cause of action.`,
  deliverables: `.  HeapSync will provide the following Deliverables: 
3.1.	Current State Analysis report of existing systems, data flows, and identified opportunities for improvement.
3.2.	Technical Assessment report with detailed evaluation of current architecture, including integration analysis and technology stack assessment.
3.3.	Final Recommendations report of complete modernization strategy including target architecture, implementation roadmap, and strategy
`,
  timeline: `. The Services and Deliverables shall be delivered in accordance with the following schedule:
4.1.	Discovery (Weeks 1-3)
•	Stakeholder interviews
•	System documentation review
•	Initial findings compilation
4.2.	Technical Analysis (Weeks 4-5)
•	Architecture evaluation
•	Integration assessment
•	Technology stack review
4.3.	Feasibility Evaluation (Weeks 6-7)
•	Gap analysis
•	Recommendations
4.4.	Final Recommendations (Weeks 8-10)
•	Roadmap development
•	Final deliverable preparation
`,
}

const SOWGenerator = () => {
  const [formData, setFormData] = useState<SOWFormData>( {
    sowType: "",
    workType: "",
    projectObjectives: "",
    projectScope: "",
    servicesDescription: "",
    specificFeatures: "",
    platformsTechnologies: "",
    integrations: "",
    designSpecifications: "",
    outOfScope: "",
    deliverables: "",
    timeline: "",
  });
  const [isGenerating, setIsGenerating] = useState(false);
  const [isLikeLoading, setIsLikeLoading] = useState(false);
  const [isChaGenerating, setIsChaGenerating] = useState(false);
  const [generatedContent, setGeneratedContent] = useState("");
  const { toast } = useToast();
  const [chatMessages, setChatMessages] = useState<{role: 'user' | 'assistant', content: string}[]>([]);
  const [chatInput, setChatInput] = useState("");
  const chatEndRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [chatMessages]);

  const handleChange = (field: keyof SOWFormData) => (
    e: React.ChangeEvent<HTMLTextAreaElement>
  ) => {
    setFormData((prev) => ({
      ...prev,
      [field]: e.target.value,
    }));
  };

  const handleSelectChange = (field: keyof SOWFormData) => (value: string) => {
    setFormData((prev) => ({
      ...prev,
      [field]: value,
    }));
  };

  const handleDownloadDocx = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/static/Generated_SOW_final.docx`, {
        responseType: 'blob', // very important to receive binary data
      });
  
      const blob = new Blob([response.data], { type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' });
  
      // Create a local URL and download link (if you want to prompt user to download)
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'Generated_SOW_final.docx'); // filename
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
  
      // OR if you want to convert to text/markdown, you can use something like mammoth:
      // const arrayBuffer = await blob.arrayBuffer();
      // const result = await mammoth.convertToMarkdown({ arrayBuffer });
      // setGeneratedContent(result.value); // if you're previewing markdown
  
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to download DOCX file",
        variant: "destructive",
      });
      console.error(error);
    }
  };
  

  const handleGenerate = async () => {
    if (!formData.projectObjectives.trim()) {
      toast({
        title: "Error",
        description: "Project Objectives is required",
        variant: "destructive",
      });
      return;
    }
    setIsGenerating(true);

    try {
      // Gather form data from state variables (Ensure these exists)
        // Send a POST request to Flask backend
        const response = await axios.post(`${API_BASE_URL}/generate-sow`, formData, {
          headers: {
            'Content-Type': 'application/json',
          },    
        });

      if (response.status === 200) {
        setGeneratedContent(response.data.message)
        toast({
          title: "Success",
          description: "SOW has been generated",
        });
        // Handle success (e.g., show a message or trigger file download)
      }
      setIsGenerating(false);
    } catch (error) {
      setIsGenerating(false);
      toast({
        title: "Error",
        description: error?.message || 'Some error occurred while generating SOW',
        variant: "destructive",
      });
    }
  };

  const handleExport = () => {
    // Export2Word("exported_document", generatedContent)
    handleDownloadDocx()
  };

  const handleLikeSOW = async () => {
    setIsLikeLoading(true);
    try {
      const response = await axios.post(`${API_BASE_URL}/like-sow`, {
        content: generatedContent,
      });

      if (response.status === 200) {
        toast({
          title: "Success",
          description: "SOW liked successfully",
        });
      }
      setIsLikeLoading(false);
    } catch (error) {
      setIsLikeLoading(false);
      toast({
        title: "Error",
        description: error?.message || 'Some error occurred while liking SOW',
        variant: "destructive",
      });
    }
  };

  const handleSendMessage = () => {
    setIsGenerating(true);
    setIsChaGenerating(true);
    if (!chatInput.trim()) return;
    const userMsg = { role: 'user' as const, content: chatInput };
    setChatMessages((prev) => [...prev, userMsg]);
    setChatInput("");
    // Send message to backend
    axios.post(`${API_BASE_URL}/chat`, {
      message: chatInput,
      context: generatedContent,
    })
    .then((response) => {
      setGeneratedContent(response.data.message);
      setIsChaGenerating(false);
      setIsGenerating(false);
    }
    )
    .catch((error) => {
      setIsGenerating(false);
      setIsChaGenerating(false);
      toast({
        title: "Error",
        description: error?.message || 'Some error occurred while sending message',
        variant: "destructive",
      });
    }
    );
  };

  return (
    <ResizablePanelGroup direction="horizontal" className="min-h-[600px] max-h-[85vh] rounded-lg border">
      <ResizablePanel defaultSize={40} minSize={30}>
        <ScrollArea className="h-full">
          <div className="p-6 space-y-6">
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="sowType" className="text-base">SOW Type</Label>
                <Select
                  value={formData.sowType}
                  onValueChange={handleSelectChange("sowType")}
                >
                  <SelectTrigger id="sowType">
                    <SelectValue placeholder="Select SOW type" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="fixed">Fixed Price</SelectItem>
                    <SelectItem value="tm">Time & Material</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="workType" className="text-base">Work Type</Label>
                <Select
                  value={formData.workType}
                  onValueChange={handleSelectChange("workType")}
                >
                  <SelectTrigger id="workType">
                    <SelectValue placeholder="Select work type" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="discovery">Discovery</SelectItem>
                    <SelectItem value="implementation">Implementation</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="projectObjectives" className="text-base font-semibold">
                Project Objectives <span className="text-red-500">*</span>
              </Label>
              <Textarea
                id="projectObjectives"
                placeholder="Enter the main objectives of the project..."
                value={formData.projectObjectives}
                onChange={handleChange("projectObjectives")}
                className="min-h-[100px]"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="projectScope" className="text-base">Project Scope</Label>
              <Textarea
                id="projectScope"
                placeholder="Define the scope of the project..."
                value={formData.projectScope}
                onChange={handleChange("projectScope")}
                className="min-h-[100px]"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="servicesDescription" className="text-base">
                Detailed Description of Services
              </Label>
              <Textarea
                id="servicesDescription"
                placeholder="Describe the services to be provided..."
                value={formData.servicesDescription}
                onChange={handleChange("servicesDescription")}
                className="min-h-[100px]"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="specificFeatures" className="text-base">
                Specific Features
              </Label>
              <Textarea
                id="specificFeatures"
                placeholder="List specific features if applicable..."
                value={formData.specificFeatures}
                onChange={handleChange("specificFeatures")}
                className="min-h-[100px]"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="platformsTechnologies" className="text-base">
                Platforms and Technologies
              </Label>
              <Textarea
                id="platformsTechnologies"
                placeholder="Specify platforms and technologies to be used..."
                value={formData.platformsTechnologies}
                onChange={handleChange("platformsTechnologies")}
                className="min-h-[100px]"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="integrations" className="text-base">Integrations</Label>
              <Textarea
                id="integrations"
                placeholder="List required integrations..."
                value={formData.integrations}
                onChange={handleChange("integrations")}
                className="min-h-[100px]"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="designSpecifications" className="text-base">
                Design Specifications
              </Label>
              <Textarea
                id="designSpecifications"
                placeholder="Enter design specifications if applicable..."
                value={formData.designSpecifications}
                onChange={handleChange("designSpecifications")}
                className="min-h-[100px]"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="outOfScope" className="text-base">Out of Scope</Label>
              <Textarea
                id="outOfScope"
                placeholder="Specify what is not included in the scope..."
                value={formData.outOfScope}
                onChange={handleChange("outOfScope")}
                className="min-h-[100px]"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="deliverables" className="text-base">Deliverables</Label>
              <Textarea
                id="deliverables"
                placeholder="List specific deliverables, quantities, and formats..."
                value={formData.deliverables}
                onChange={handleChange("deliverables")}
                className="min-h-[100px]"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="timeline" className="text-base">Project Timeline & Schedule</Label>
              <Textarea
                id="timeline"
                placeholder="Outline the project timeline and schedule..."
                value={formData.timeline}
                onChange={handleChange("timeline")}
                className="min-h-[100px]"
              />
            </div>

            <div className="sticky bottom-0 pt-4 bg-background">
              <Button
                onClick={handleGenerate}
                disabled={isGenerating || !formData.projectObjectives.trim()}
                className="w-full mb-2"
              >
                {isGenerating ? (
                  <>
                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                    Generating
                  </>
                ) : (
                  "Generate"
                )}
              </Button>
            </div>
          </div>
        </ScrollArea>
      </ResizablePanel>

      <ResizableHandle withHandle />

      <ResizablePanel defaultSize={60}>
        <div className="p-6 h-full">
          {generatedContent ? (
            <div className="space-y-4 h-full flex flex-col">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-semibold">Generated SOW</h3>
                <div className="flex items-center space-x-2">
                  <Button variant="outline" onClick={handleLikeSOW} disabled={isLikeLoading}>
                    {isLikeLoading ? (
                      <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                    ) : (
                      <ThumbsUp className="w-4 h-4" />
                    )}
                  </Button>
                  <Button variant="outline" disabled>
                      <ThumbsDown className="w-4 h-4" />
                  </Button>
                  <Button variant="outline" onClick={handleExport}>
                    <Download className="w-4 h-4 mr-2" />
                    Export to Word
                  </Button>
                </div>
              </div>
               {/* Chat Interface */}
               <div className="mt-4 border rounded-lg bg-muted p-4 flex flex-col max-h-[10rem]">
                <div className="flex-1 overflow-y-auto mb-2 space-y-2">
                  {chatMessages.map((msg, idx) => (
                    <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                      <div className={`rounded-lg px-3 py-2 max-w-[80%] text-sm ${msg.role === 'user' ? 'bg-primary text-primary-foreground' : 'bg-background border'}`}>
                        {msg.content}
                      </div>
                    </div>
                  ))}
                  <div ref={chatEndRef} />
                </div>
                <div className="flex gap-2">
                  <input
                    type="text"
                    className="flex-1 border rounded px-2 py-1 text-sm"
                    placeholder="Ask AI to refine your SOW..."
                    value={chatInput}
                    onChange={e => setChatInput(e.target.value)}
                    onKeyDown={e => { if (e.key === 'Enter') handleSendMessage(); }}
                    disabled={!generatedContent}
                  />
                  <Button
                    onClick={handleSendMessage}
                    disabled={isChaGenerating || !chatInput.trim() || !generatedContent}
                    size="sm">
                      {isChaGenerating ? 'Refining...' : 'Send'}
                    </Button>
                </div>
              </div>
              <Card className="p-6 h-[calc(100%-15rem)] overflow-auto flex-1">
                <div className="prose max-w-none">
                {isChaGenerating ? (
                  <div className="flex items-center justify-center">
                    <Loader2 className="w-6 h-6 animate-spin" />
                  </div>
                ) : (
                  <MarkdownPreview source={generatedContent} />
                )}
                </div>
              </Card>
            </div>
          ) : (
            <div className="h-full flex items-center justify-center text-muted-foreground">
              {isGenerating ? (
                <Loader2 className="w-6 h-6 animate-spin" />
              ) : (
                'Generated content will appear here'       
              )}
            </div>
          )}
        </div>
      </ResizablePanel>
    </ResizablePanelGroup>
  );
};

export default SOWGenerator;
