
import { useState } from "react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Card } from "@/components/ui/card";
import { FileText, Settings } from "lucide-react";
import SOWGenerator from "@/components/SOWGenerator";
import ModelConfig from "@/components/ModelConfig";
import { Navbar } from "@/components/ui/navbar";

const Index = () => {
  const [activeTab, setActiveTab] = useState("generator");

  return (
    <div className="min-h-screen bg-background p-3 animate-fade-in">
      <Navbar />
      <div className="max-w-7xl mx-auto space-y-6 mt-4">
          <SOWGenerator />
      </div>
    </div>
  );
};

export default Index;
